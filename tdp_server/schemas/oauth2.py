from typing import List, Optional

from fastapi import Form
from pydantic import AnyHttpUrl, BaseModel, validator

SUPPORTED_GRANT_TYPES = ["password", "authorization_code"]
SCOPES = {
    "tdp_server:read": "Allow get operations",
    "tdp_server:write": "Allow post/put/patch operations",
    "tdp_server:execute": "Allow deployment operations",
}

class OAuth2TokenRequest:
    def __init__(
        self,
        grant_type: str = Form(None, regex="|".join(SUPPORTED_GRANT_TYPES)),
        username: Optional[str] = Form(None),
        password: Optional[str] = Form(None),
        code: Optional[str] = Form(None),
        scope: Optional[str] = Form(None),
        client_id: str = Form(...),
        client_secret: Optional[str] = Form(None),
        redirect_uri: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        if grant_type == "password":
            self.username = username
            self.password = password
        elif grant_type == "authorization_code":
            self.code = code
        self.scopes = scope.split() if scope is not None else None
        self.client_id = client_id
        if client_secret:
            self.client_secret = client_secret
        self.redirect_uri = redirect_uri


class CreateClient(BaseModel):
    client_name: str
    client_uri: AnyHttpUrl
    grant_types: List[str] = SUPPORTED_GRANT_TYPES
    redirect_uris: List[AnyHttpUrl]
    response_types: List[str] = ["code", "token", "code token"]
    scopes: List[str]
    token_endpoint_auth_method: str = "none"

    @validator("grant_types")
    def grant_types_validator(cls, grant_types, values):
        if len(grant_types) == 0:
            raise ValueError("Cannot create a client without grant types")
        unsupported_grant_types = set(grant_types).difference(SUPPORTED_GRANT_TYPES)
        if unsupported_grant_types:
            raise ValueError(
                f"{', '.join(unsupported_grant_types)} are not supported grant types."
            )
        return grant_types


class OAuth2Client(BaseModel):
    client_id: str
    # client_secret: str # We should never return the client secret
    client_id_issued_at: int
    client_secret_expires_at: Optional[str] = None
    client_name: str
    client_uri: str
    grant_types: List[str] = []
    redirect_uris: List[str] = []
    response_types: List[str] = []
    scopes: Optional[List[str]] = None
    token_endpoint_auth_method: str = "none"
