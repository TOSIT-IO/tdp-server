from pydantic import BaseModel
from typing import Optional, List

from tdp_server.schemas.variables import Variables


class ServiceOrComponentUpdateResponse(BaseModel):
    message: str


class CommonOptions(BaseModel):
    collections: List[str]
    database_dsn: str
    validate_vars: Optional[bool] = False
    variables: str
