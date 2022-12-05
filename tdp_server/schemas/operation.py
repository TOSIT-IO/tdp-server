from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, validator
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

    class Config:
        orm_mode = True

    @validator("start_time", "end_time")
    def validate_datetimes(cls, dt, values):
        if dt is not None:
            return dt.replace(tzinfo=timezone.utc)
        return dt
