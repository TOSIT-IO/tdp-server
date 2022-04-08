from typing import Optional

from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App
from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes
from fastapi.security.open_id_connect_url import OpenIdConnect
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt

from tdp_server.core.config import settings

SUPPORTED_ALGORITHMS_KEY = "id_token_signing_alg_values_supported"

# TODO: Gérer la possibilité de se connecter directement à l'API et get l'access token depuis elle ?

authlib_oauth = OAuth()
authlib_oauth.register(
    name="sso_backend",
    server_metadata_url=settings.OPENID_CONNECT_DISCOVERY_URL,
    client_kwargs={"scope": "openid"},
    client_id=settings.OPENID_CLIENT_ID,
    # client_secret=settings.OPENID_CLIENT_SECRET,
)

openid_connect = OpenIdConnect(
    openIdConnectUrl=settings.OPENID_CONNECT_DISCOVERY_URL,
    auto_error=False,
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


async def issuer_public_key(
    oauth_client: StarletteOAuth2App = Depends(get_authlib_client),
):
    return await oauth_client.fetch_jwk_set()


async def validate_token(
    security_scopes: SecurityScopes,
    authorization: Optional[str] = Depends(openid_connect),
    metadata: dict = Depends(issuer_metadata),
    public_key: str = Depends(issuer_public_key),
):
    token_info = None
    try:
        if authorization:
            scheme, token = get_authorization_scheme_param(authorization)
            if scheme.lower() != "bearer":
                raise Exception("invalid authentication type")
            token_info = jwt.decode(
                token,
                public_key,
                algorithms=metadata[SUPPORTED_ALGORITHMS_KEY],
                audience=settings.OPENID_CLIENT_ID,
                issuer=metadata["issuer"],
            )
        else:
            raise Exception("no authentication supplied")
    except Exception as exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error during authentication validation ({exp})",
            headers={"WWW-Authenticate": f"Bearer"},
        )

    for scope in security_scopes.scopes:
        if scope not in token_info["scope"].split(" "):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": f"Bearer {security_scopes.scope_str}"},
            )
