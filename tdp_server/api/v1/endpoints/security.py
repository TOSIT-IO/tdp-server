import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from authlib.integrations.base_client.errors import MismatchingStateError
from authlib.integrations.starlette_client import StarletteOAuth2App
from authlib.oauth2.auth import OAuth2Token
from authlib.oauth2.rfc6749 import OAuth2Request
from fastapi import APIRouter, Depends, HTTPException, Request, status
from jose import jwt
from sqlalchemy.orm import Session

from tdp_server import schemas
from tdp_server.api import dependencies
from tdp_server.core.config import Settings
from tdp_server.schemas import CreateClient, OAuth2TokenRequest
from tdp_server.services import UserService
from tdp_server.services.oauth2 import (
    AuthorizationServer,
    ClientService,
    to_oauth2_request,
)

logger = logging.getLogger("tdp_server")
router = APIRouter()

STATE_TOKEN_EXPIRATION = 5 * 60
AUTHORIZATION_CODE_EXPIRATION = 5 * 60


def encode_jwt(
    data: Dict[str, Any], secret: str, audience: str, lifetime: int, algorithm: str
) -> str:
    expire = datetime.utcnow() + timedelta(seconds=lifetime)
    data["exp"] = expire
    data["aud"] = audience
    return jwt.encode(data, secret, algorithm)


def decode_jwt(token: str, secret: str, audience: str, algorithms: list):
    return jwt.decode(token, secret, audience=audience, algorithms=algorithms)


async def authorize_callback(
    request: Request,
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    *,
    oauth2: StarletteOAuth2App = Depends(dependencies.get_authlib_client),
) -> Tuple[OAuth2Token, Optional[str]]:
    if code is None or error is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    try:
        access_token = await oauth2.authorize_access_token(request)
    except MismatchingStateError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return access_token, state


@router.get("/authorize", name="auth:authorize")
async def authorize(
    request: Request,
    client_id: str,
    state: str,
    scope: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    client_secret: Optional[str] = None,
    *,
    db: Session = Depends(dependencies.get_db),
    oauth2: StarletteOAuth2App = Depends(dependencies.get_authlib_client),
    settings: Settings = Depends(dependencies.get_settings),
):
    if ClientService.get_client(db, client_id) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client id submitted",
        )
    state_data = {
        "scope": scope,
        "redirect_uri": redirect_uri,
        "url": str(request.url),
        "state": state,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    redirect_uri = request.url_for("auth:callback")
    state = encode_jwt(
        state_data,
        settings.SECRET_KEY,
        settings.OPENID_CLIENT_ID,
        STATE_TOKEN_EXPIRATION,
        settings.ALGORITHM,
    )
    return await oauth2.authorize_redirect(
        request, redirect_uri, state=state, scope="openid"
    )


@router.get("/callback", name="auth:callback")
async def callback(
    access_token_state: Tuple[OAuth2Token, str] = Depends(authorize_callback),
    *,
    authorization: AuthorizationServer = Depends(dependencies.get_authorization),
    db: Session = Depends(dependencies.get_db),
    settings: Settings = Depends(dependencies.get_settings),
):
    token, state = access_token_state
    try:
        state = decode_jwt(
            state, settings.SECRET_KEY, settings.OPENID_CLIENT_ID, [settings.ALGORITHM]
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to decode state data",
        )

    try:
        user = UserService.oauth2_callback(db, token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to connect ({e})"
        )
    oauth2_request = OAuth2Request("GET", state["url"], state)
    return authorization.create_authorization_response(
        request=oauth2_request, grant_user=user
    )


@router.post("/token", name="auth:token")
async def token(
    request: Request,
    auth_form: OAuth2TokenRequest = Depends(),
    *,
    authorization: AuthorizationServer = Depends(dependencies.get_authorization),
) -> Any:
    oauth2_request = await to_oauth2_request(request, auth_form)
    try:
        return authorization.create_token_response(oauth2_request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/client",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.OAuth2Client,
)
def create_client(
    create_client: CreateClient,
    *,
    db: Session = Depends(dependencies.get_db),
) -> Any:
    client = ClientService.create_client(db, create_client)
    return schemas.OAuth2Client(**client.client_info, **client.client_metadata)


@router.get("/client", response_model=List[schemas.OAuth2Client])
def get_clients(db: Session = Depends(dependencies.get_db)) -> Any:
    clients = ClientService.get_clients(db)
    clients = map(
        lambda client: schemas.OAuth2Client(
            **client.client_info, **client.client_metadata
        ),
        clients,
    )

    return list(clients)
