from datetime import datetime

from pydantic import BaseModel
from tdp.core.runner.executor import StateEnum


class Operation(BaseModel):
    operation: str
    start: datetime
    end: datetime
    state: StateEnum
    logs: bytes
