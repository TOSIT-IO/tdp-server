from typing import Generator, Optional

from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App
from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.openapi.models import (
    OAuthFlowAuthorizationCode,
    OAuthFlowImplicit,
    OAuthFlowPassword,
    OAuthFlows,
)
from fastapi.security import OAuth2, SecurityScopes
from tdp.core.collections import Collections
from tdp.core.dag import Dag
from tdp.core.deployment import DeploymentRunner
from tdp.core.variables import ClusterVariables

from tdp_server.core.config import Settings, settings
from tdp_server.db.session import SessionLocal
from tdp_server.models.oauth2 import OAuth2Token
from tdp_server.schemas import SCOPES
from tdp_server.services import RunnerService
from tdp_server.services.oauth2 import AuthorizationServer, ResourceProtector
from tdp_server.services.oauth2.utils import to_oauth2_request

COMMON_RESPONSES = {
    401: {
        "description": "Unauthenticated",
        "content": {
            "application/json": {
                "example": {"detail": "Error during authentication validation (reason)"}
            }
        },
    },
    403: {
        "description": "Not enough privileges",
        "headers": {
            "WWW-Authenticate": {
                "schema": {"type": "string"},
                "description": "Authentication method to use",
            }
        },
        "content": {
            "application/json": {"example": {"detail": "Not enough permissions"}}
        },
    },
}

authlib_oauth = OAuth()
authlib_oauth.register(
    name="sso_backend",
    server_metadata_url=settings.OPENID_CONNECT_DISCOVERY_URL,
    client_kwargs={"scope": "openid"},
    client_id=settings.OPENID_CLIENT_ID,
    # client_secret=settings.OPENID_CLIENT_SECRET,
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


def get_db() -> Generator:
    with SessionLocal() as db:
        yield db


def get_dag(request: Request) -> Dag:
    return request.app.state.dag


def get_cluster_variables(request: Request) -> ClusterVariables:
    return request.app.state.cluster_variables


def get_deployment_runner(request: Request) -> DeploymentRunner:
    return request.app.state.deployment_runner


def get_collections(request: Request) -> Collections:
    return request.app.state.settings.TDP_COLLECTIONS


def get_runner_service(request: Request) -> RunnerService:
    return request.app.state.runner_service


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_authorization(request: Request) -> AuthorizationServer:
    return request.app.state.authorization


def get_protector(request: Request) -> ResourceProtector:
    return request.app.state.protector


OAUTH2_SCHEME = OAuth2(
        flows=OAuthFlows(
            authorizationCode=OAuthFlowAuthorizationCode(
                authorizationUrl="/api/v1/security/authorize",
                tokenUrl="/api/v1/security/token",
                scopes=SCOPES,
            ),
            # implicit=OAuthFlowImplicit(
            #     authorizationUrl="/auth",
            #     scopes=SCOPES,
            # ),
            # password=OAuthFlowPassword(
            #     tokenUrl="/token",
            #     scopes=SCOPES,
            # ),
        )
    )


def get_oauth2_client(
    metadata: dict = Depends(issuer_metadata),
    settings: Settings = Depends(get_settings),
) -> AsyncOAuth2Client:
    oauth2 = AsyncOAuth2Client(
        token_endpoint=metadata["token_endpoint"],
        client_id=settings.OPENID_CLIENT_ID,
        client_secret=settings.OPENID_CLIENT_SECRET,
        scope="openid email profile",
    )
    return oauth2


async def validate_token(
    request: Request,
    security_scopes: SecurityScopes,
    protector: ResourceProtector = Depends(get_protector),
    _authorization: Optional[str] = Depends(OAUTH2_SCHEME),
) -> OAuth2Token:
    try:
        token = protector.acquire_token(request, security_scopes.scopes)
    except Exception as exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error during authentication validation ({exp})",
            headers={"WWW-Authenticate": f"Bearer"},
        )

    return token


async def read_protected(
        token: OAuth2Token = Security(validate_token, scopes=[settings.SCOPE_NAMESPACE + ":read"])
) -> str:
    return token.user_id  # type: ignore


async def write_protected(
    token: OAuth2Token = Security(validate_token, scopes=[settings.SCOPE_NAMESPACE + ":write"])
) -> str:
    return token.user_id  # type: ignore


async def execute_protected(
    token: OAuth2Token = Security(validate_token, scopes=[settings.SCOPE_NAMESPACE + ":write"])
) -> str:
    return token.user_id  # type: ignore
