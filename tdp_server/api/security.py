import logging
from datetime import datetime, timedelta
from typing import Any, Mapping, Optional

from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.integrations.starlette_client import OAuth, OAuthError, StarletteOAuth2App
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.openapi.models import (
    OAuthFlowAuthorizationCode,
    OAuthFlowImplicit,
    OAuthFlowPassword,
    OAuthFlows,
)
from fastapi.security import OAuth2, OAuth2PasswordRequestFormStrict, SecurityScopes
from fastapi.security.utils import get_authorization_scheme_param
from httpx import HTTPStatusError
from jose import jwt
from starlette.datastructures import QueryParams
from starlette.responses import RedirectResponse

from tdp_server.core.config import settings

logger = logging.getLogger("tdp_server")
router = APIRouter()

# OAuth 2 definitions

SUPPORTED_ALGORITHMS_KEY = "id_token_signing_alg_values_supported"

SCOPES = {
    "tdp_server:read": "Allow get operations",
    "tdp_server:write": "Allow post/put/patch operations",
    "tdp_server:execute": "Allow deployment operations",
}


OAUTH2_SCHEME = OAuth2(
    flows=OAuthFlows(
        authorizationCode=OAuthFlowAuthorizationCode(
            authorizationUrl="/auth",
            tokenUrl="token",
            scopes=SCOPES,
        ),
        implicit=OAuthFlowImplicit(
            authorizationUrl="/auth",
            scopes=SCOPES,
        ),
        password=OAuthFlowPassword(
            tokenUrl="/token",
            scopes=SCOPES,
        ),
    )
)
SUPPORTED_GRANT_TYPES = ["password", "authorization_code"]


class OAuth2TokenRequest:
    def __init__(
        self,
        grant_type: str = Form(None, regex="|".join(SUPPORTED_GRANT_TYPES)),
        username: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        code: Optional[str] = Form(None),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        if grant_type == "password":
            self.username = username
            self.password = password
        elif grant_type == "authorization_code":
            self.code = code
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


# authlib client

authlib_oauth = OAuth()
authlib_oauth.register(
    name="sso_backend",
    server_metadata_url=settings.OPENID_CONNECT_DISCOVERY_URL,
    client_kwargs={"scope": "openid email profile"},
    client_id=settings.OPENID_CLIENT_ID,
    client_secret=settings.OPENID_CLIENT_SECRET,
)


def get_authlib_client() -> StarletteOAuth2App:
    oauth_client = authlib_oauth.create_client("sso_backend")
    if not oauth_client:
        raise Exception("Failed to create OAuth client")
    return oauth_client


async def issuer_metadata(
    oauth_client: StarletteOAuth2App = Depends(get_authlib_client),
):
    return await oauth_client.load_server_metadata()


def get_authlib_oauth2_client(
    metadata: dict = Depends(issuer_metadata),
) -> AsyncOAuth2Client:
    oauth2 = AsyncOAuth2Client(
        token_endpoint=metadata["token_endpoint"],
        client_id=settings.OPENID_CLIENT_ID,
        client_secret=settings.OPENID_CLIENT_SECRET,
        scope="openid email profile",
    )
    return oauth2


def mock_validate_token(
    security_scopes: SecurityScopes,
    authorization: Optional[str] = Depends(OAUTH2_SCHEME),
) -> Mapping:
    return {"sub": "fake_user_from_mock_validate_token"}


def validate_token(
    security_scopes: SecurityScopes,
    authorization: Optional[str] = Depends(OAUTH2_SCHEME),
) -> Mapping:
    token_info = None
    try:
        if authorization:
            scheme, token = get_authorization_scheme_param(authorization)
            if scheme.lower() != "bearer":
                raise Exception("invalid authentication type")
            token_info = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=settings.ALGORITHM,
            )
        else:
            raise Exception("no authentication supplied")
    except Exception as exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error during authentication validation ({exp})",
            headers={"WWW-Authenticate": "Bearer"},
        )

    for scope in security_scopes.scopes:
        if scope not in token_info["scope"].split(" "):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": f"Bearer {security_scopes.scope_str}"},
            )
    return token_info


if settings.DO_NOT_USE_IN_PRODUCTION_DISABLE_TOKEN_CHECK:
    logger.warn("Token validation is disabled. Do not do this in production.")
    validate_token = mock_validate_token


### utilities
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


### security endpoints
@router.get("/auth")
async def auth(
    request: Request,
    redirect_uri: Optional[str] = None,
    state: Optional[str] = None,
    authlib_client: StarletteOAuth2App = Depends(get_authlib_client),
) -> Any:
    original_data = {}  # in case we need to re-redirect
    print(request.query_params)
    if all((redirect_uri, state)):
        original_data = {"original_redirect_uri": redirect_uri, "original_state": state}
    redirect_uri = request.url_for("callback")
    return await authlib_client.authorize_redirect(
        request, redirect_uri, **original_data
    )


@router.get("/callback")
async def callback(
    request: Request,
    authlib_client: StarletteOAuth2App = Depends(get_authlib_client),
) -> Any:

    state_data = await authlib_client.framework.get_state_data(
        request.session, request.query_params.get("state")
    )
    query_params = QueryParams(state_data["url"])
    original_redirect_uri = query_params.get("original_redirect_uri")
    original_state = query_params.get("original_state")
    try:
        oidc_access_token = await authlib_client.authorize_access_token(request)
    except HTTPStatusError as e:
        logger.error("Failed to validate access token, check your OIDC configuration")
        logger.exception(e)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="check server logs to investigate error",
        )
    except OAuthError as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if all((original_redirect_uri, original_state)):
        return RedirectResponse(
            original_redirect_uri + "?state=" + original_state + "&code=91",
            status_code=302,
        )
    userinfo = oidc_access_token["userinfo"]
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=userinfo, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token")
async def token(
    auth_form: OAuth2TokenRequest = Depends(),
    authlib_client: StarletteOAuth2App = Depends(get_authlib_client),
    oauth2_client: AsyncOAuth2Client = Depends(get_authlib_oauth2_client),
) -> Any:
    print(auth_form.__dict__)

    if not "openid" in auth_form.scopes:
        auth_form.scopes.append("openid")
    auth_form.__dict__.pop("scopes")
    try:
        oidc_access_token = await oauth2_client.fetch_token(
            response_type="id_token",
            **auth_form.__dict__,
        )  # type: ignore
    except HTTPStatusError as e:
        logger.error("Failed to fetch access token, check your OIDC configuration")
        logger.exception(e)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="check server logs to investigate error",
        )
    userinfo = await authlib_client.parse_id_token(oidc_access_token, nonce=None)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=userinfo, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
