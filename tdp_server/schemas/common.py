from pydantic import BaseModel
from typing import Optional, List


class ServiceOrComponentUpdateResponse(BaseModel):
    message: str


class CommonOptions(BaseModel):
    collections: List[str]
    database_dsn: str
    validate_vars: Optional[bool] = False
    variables: str
