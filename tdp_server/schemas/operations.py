from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from tdp.core.utils import BaseEnum
from tdp.core.models.state_enum import DeploymentStateEnum


class Operationtype(BaseEnum):
    DAG = "Dag"
    OTHER = "Other"


# class Operation(BaseModel):
#     name: str
#     type: Operationtype
#     collection_name: Optional[str] = None
#     depends_on: List[str] = []
#     noop: bool = False
#     service: str
#     action: str
#     component: Optional[str] = None
    
class Operation(BaseModel):
    operation: str
    hosts: Optional[set[str]]


class OperationLog(BaseModel):
    operation: str
    start_time: datetime
    end_time: datetime
    status: DeploymentStateEnum
    logs: bytes
