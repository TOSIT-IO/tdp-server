from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from tdp.core.models import StateEnum


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
    state: StateEnum
    logs: bytes
