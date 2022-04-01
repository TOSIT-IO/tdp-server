from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from tdp.core.models.state_enum import DeploymentStateEnum
from tdp.core.models.deployment_model import DeploymentTypeEnum
from tdp_server.schemas.plan import PlanOperations


class DeploymentLog(BaseModel):
    id: int
    options: Optional[dict]
    start_time: datetime
    end_time: Optional[datetime] = None
    restart: bool = False
    status: DeploymentStateEnum
    deployment_type: DeploymentTypeEnum
    deployment_url: str
    operations: List[PlanOperations]
    user: Optional[str] = "NO_USER_RECORDED"
