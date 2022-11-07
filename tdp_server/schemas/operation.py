from datetime import datetime

from pydantic import BaseModel
from tdp.core.models import StateEnum


class Operation(BaseModel):
    operation: str
    start_time: datetime
    end_time: datetime
    state: StateEnum
    logs: bytes
