from pydantic import BaseModel

from tdp_server.schemas.variables import Variables


class ServiceOrComponentUpdate(BaseModel):
    message: str
    variables: Variables


class ServiceOrComponentUpdateResponse(BaseModel):
    message: str
    version: str
