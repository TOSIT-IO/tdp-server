import functools
from contextlib import contextmanager
from typing import Any, List, Optional

from authlib import oauth2
from fastapi import HTTPException, Request
from sqlalchemy.orm import sessionmaker

from tdp_server.models.oauth2 import OAuth2Token


class ResourceProtector(oauth2.ResourceProtector):
    def acquire_token(
        self, request: Request, scope: Optional[List[str]] = None
    ) -> OAuth2Token:
        http_request = oauth2.HttpRequest(
            request.method, request.url, {}, request.headers
        )
        token = self.validate_request(scope, http_request)
        request.state.token = token
        return token

    @contextmanager
    def acquire(self, request: Request, scope: Optional[List[str]] = None):
        try:
            yield self.acquire_token(request, scope)
        except oauth2.OAuth2Error as error:
            raise_error_response(error)

    def __call__(
        self, scope: Optional[List[str]] = None, optional: bool = False
    ) -> Any:
        def wrapper(func):
            @functools.wraps(func)
            def decorated(request, *args, **kwargs):
                try:
                    self.acquire_token(request, scope)
                except oauth2.rfc6749.MissingAuthorizationError as e:
                    if not optional:
                        raise_error_response(e)
                except oauth2.OAuth2Error as e:
                    raise_error_response(e)
                return func(request, *args, **kwargs)

            return decorated

        return wrapper


def raise_error_response(error: oauth2.OAuth2Error):
    raise HTTPException(
        status_code=error.status_code,
        detail=dict(error.get_body()),
        headers=dict(error.get_headers()),
    )


def create_bearer_token_validator(db: sessionmaker):
    from authlib.oauth2.rfc6750 import BearerTokenValidator

    class _BearerTokenValidator(BearerTokenValidator):
        def authenticate_token(self, token_string):
            with db() as session:
                return (
                    session.query(OAuth2Token)
                    .filter_by(access_token=token_string)
                    .first()
                )

        def request_invalid(self, request):
            return False

        def token_revoked(self, token):
            return token.revoked

    return _BearerTokenValidator


def configure_resource_protector(
    session: sessionmaker, resource_protector: ResourceProtector
):

    bearer_validator = create_bearer_token_validator(session)
    resource_protector.register_token_validator(bearer_validator())
