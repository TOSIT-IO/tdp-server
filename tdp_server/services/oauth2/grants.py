from typing import Optional
from authlib.oauth2 import OAuth2Request

from authlib.oauth2.rfc6749 import grants
from sqlalchemy import desc

from tdp_server.models import OAuth2AuthorizationCode, OAuth2Client, OAuth2Token, User


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = ["none", "client_secret_basic", "client_secret_post"]

    def save_authorization_code(self, code: str, request: OAuth2Request):
        auth_code = OAuth2AuthorizationCode(
            code=code,
            client_id=self.client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_id=request.user.id,
        )
        with self.server.db() as session:
            session.add(auth_code)
            session.commit()

    def query_authorization_code(
        self, code: str, client: OAuth2Client
    ) -> OAuth2AuthorizationCode:
        with self.server.db() as session:
            auth_code = (
                session.query(OAuth2AuthorizationCode)
                .filter(
                    OAuth2AuthorizationCode.code == code,
                    OAuth2AuthorizationCode.client_id == client.client_id,
                )
                .order_by(desc(OAuth2AuthorizationCode.id))
                .first()
            )

        if auth_code is None:
            raise ValueError("Authorization code not found")
        if auth_code.is_expired():
            raise ValueError("Authorization code is expired")

        return auth_code

    def delete_authorization_code(self, authorization_code: OAuth2AuthorizationCode):
        with self.server.db() as session:
            session.delete(authorization_code)
            session.commit()

    def authenticate_user(
        self, authorization_code: OAuth2AuthorizationCode
    ) -> Optional[User]:
        with self.server.db() as session:
            return (
                session.query(User)
                .filter(User.id == authorization_code.user_id)
                .first()
            )


class RefreshTokenGrant(grants.RefreshTokenGrant):
    def authenticate_refresh_token(self, refresh_token: str) -> OAuth2Token:
        with self.server.db() as session:
            token = (
                session.query(OAuth2Token)
                .filter(OAuth2Token.refresh_token == refresh_token)
                .first()
            )
        if token is None:
            raise ValueError("Associated access token not found")

        if not token.is_refresh_token_active():
            raise ValueError("Expired refresh token")

        return token

    def authenticate_user(self, credential: OAuth2Token) -> Optional[User]:
        with self.server.db() as session:
            return session.query(User).filter(User.id == credential.user_id).first()
