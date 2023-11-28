from pydantic import BaseModel

from tdp_server.schemas.variables import Variables


class ServiceOrComponentUpdateResponse(BaseModel):
    message: str
    version: str
