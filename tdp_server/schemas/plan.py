from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

from tdp.core.models.state_enum import OperationStateEnum
from tdp.core.utils import BaseEnum


class PlanOptionsDag(BaseEnum):
    restart: Optional[bool] = False
    reverse: Optional[bool] = False
    stop: Optional[bool] = False


class PlanDag(BaseModel):
    deployment_id: int
    operation_order: int
    operation: str
    host: Optional[str]
    extra_vars: Optional[List[str]]
    start_time: Optional[datetime]
    end_time: datetime
    state: OperationStateEnum
    logs: Optional[str]
