from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel
from tdp.core.models.state_enum import DeploymentStateEnum


class Operation(BaseModel):
    name: str
    collection_name: Optional[str] = None
    depends_on: List[str] = []
    noop: bool = False
    service: str
    action: str
    component: Optional[str] = None


class OperationLog(BaseModel):
    operation: str
    start_time: datetime
    end_time: datetime
    status: DeploymentStateEnum
    logs: bytes
