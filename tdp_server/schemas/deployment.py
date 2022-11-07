from datetime import datetime
from re import compile
from typing import List, Optional

from pydantic import BaseModel, validator
from tdp.core.models import DeploymentLog, FilterTypeEnum, StateEnum

from tdp_server.schemas.operation import Operation


class DeployRequest(BaseModel):
    targets: Optional[List[str]] = None
    sources: Optional[List[str]] = None
    filter_type: Optional[FilterTypeEnum] = None
    filter_expression: Optional[str] = None
    restart: bool = False

    @validator("sources")
    def sources_validator(cls, value, values):
        if value is not None and values.get("targets") is not None:
            raise ValueError("targets and sources fields are mutually exclusive")
        return value


class DeployStatus(BaseModel):
    message: str


class Deployment(BaseModel):
    id: int
    sources: Optional[List[str]] = None
    targets: Optional[List[str]] = None
    filter_expression: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    restart: bool = False
    state: StateEnum
    operations: List[str]
    user: str


class DeploymentWithOperations(Deployment):
    operations: List[Operation]
