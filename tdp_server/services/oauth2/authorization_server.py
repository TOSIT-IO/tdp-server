from typing import Callable, List, Optional

from authlib import oauth2
from authlib.common import security
from authlib.oauth2.rfc6749 import OAuth2Request
from authlib.oauth2.rfc6750 import token
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker

from tdp_server.core.config import Settings
from tdp_server.models import OAuth2Client, OAuth2Token

from .grants import AuthorizationCodeGrant, RefreshTokenGrant


class AuthorizationServer(oauth2.AuthorizationServer):
    def __init__(self, db: sessionmaker, scopes_supported: Optional[List[str]] = None):
        super().__init__(scopes_supported)
        self.db = db

    def create_oauth2_request(self, request) -> OAuth2Request:
        if isinstance(request, OAuth2Request):
            return request
        return OAuth2Request(request.method, request.uri, request.body, request.headers)

    def create_json_request(self, request: Request) -> oauth2.HttpRequest:
        return oauth2.HttpRequest(
            request.method, str(request.url), request.body, request.headers
        )

    def handle_response(self, status, body, headers):
        return JSONResponse(status_code=status, content=body, headers=dict(headers))

    def query_client(self, client_id: str) -> OAuth2Client:
        with self.db() as session:
            return (
                session.query(OAuth2Client)
                .where(OAuth2Client.client_id == client_id)
                .first()
            )

    def save_token(self, token: dict, request: OAuth2Request):
        if request.user:
            user_id = request.user.id
        else:
            user_id = None
        client = request.client
        if client is None:
            raise Exception()
        item = OAuth2Token(client_id=client.client_id, user_id=user_id, scope=request.scope, **token)
        with self.db() as session:
            session.add(item)
            session.commit()

    def send_signal(self, name, *args, **kwargs):
        pass


def create_generate_access_token(settings: Settings) -> Callable:
    def generate_access_token(*args, **kwargs):
        return security.generate_token(settings.ACCESS_TOKEN_LENGTH)

    return generate_access_token


def create_generate_refresh_token(settings: Settings) -> Callable:
    def generate_refresh_token(*args, **kwargs):
        return security.generate_token(settings.REFRESH_TOKEN_LENGTH)

    return generate_refresh_token


def configure_authorization_server(
    settings: Settings, authorization: AuthorizationServer
):
    authorization.register_grant(AuthorizationCodeGrant)
    authorization.register_grant(RefreshTokenGrant)

    bearer_token_generator = token.BearerTokenGenerator(
        access_token_generator=create_generate_access_token(settings),
        refresh_token_generator=create_generate_refresh_token(settings),
    )
    authorization.register_token_generator(
        "default", bearer_token_generator
    )  # default token generator
