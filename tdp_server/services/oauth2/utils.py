from authlib.oauth2.rfc6749 import OAuth2Request
from fastapi import Request

from tdp_server.schemas.oauth2 import OAuth2TokenRequest


async def to_oauth2_request(
    request: Request, body: OAuth2TokenRequest
) -> OAuth2Request:
    return OAuth2Request(
        request.method, str(request.url), body.__dict__, request.headers
    )
