from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from tdp.core.runner.executor import StateEnum

from tdp_server.schemas.operation import Operation


class DeployRequest(BaseModel):
    targets: Optional[List[str]] = None
    filter_expression: Optional[str] = None
    sources: Optional[List[str]] = None


class DeployStatus(BaseModel):
    message: str


class Deployment(BaseModel):
    id: int
    sources: Optional[List[str]] = None
    targets: Optional[List[str]] = None
    filter_expression: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    state: StateEnum
    operations: List[str]
    user: str


class DeploymentWithOperations(Deployment):
    operations: List[Operation]
