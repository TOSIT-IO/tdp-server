from pydantic import BaseModel
from typing import Optional, List

from tdp.core.utils import BaseEnum


class ServiceOrComponentUpdateResponse(BaseModel):
    message: str


class CommonOptions(BaseModel):
    collections: List[str]
    database_dsn: str
    validate_vars: Optional[bool] = False
    variables: str


class StateEnum(BaseEnum):
    start = "Start"
    stop = "Stop"
