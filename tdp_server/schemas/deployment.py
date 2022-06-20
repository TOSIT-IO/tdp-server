from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from tdp.core.runner.executor import StateEnum

from tdp_server.schemas.operation import Operation


class DeployRequest(BaseModel):
    targets: Optional[List[str]] = []
    filter: Optional[str] = None
    sources: Optional[List[str]] = []


class DeployStatus(BaseModel):
    message: str


class Deployment(BaseModel):
    id: int
    sources: List[str] = []
    targets: List[str] = []
    filter: str
    start: datetime
    end: datetime
    state: StateEnum
    operations: List[str]


class DeploymentWithOperations(Deployment):
    operations: List[Operation]
