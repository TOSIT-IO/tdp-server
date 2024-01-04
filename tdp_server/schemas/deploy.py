from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from tdp.core.models.state_enum import DeploymentStateEnum
from tdp.core.models.deployment_model import DeploymentTypeEnum
from tdp_server.schemas.plan import PlanOperations


class DeployStatus(BaseModel):
    message: str

    class Config:
        json_schema_extra = {"example": {"message": "Deployment successful"}}


class DeploymentStart(BaseModel):
    id: int
    options: Optional[dict]
    start_time: datetime
    restart: bool = False
    status: DeploymentStateEnum
    deployment_type: DeploymentTypeEnum
    deployment_url: str
    operations: List[PlanOperations]
    user: Optional[str] = "NO_USER_RECORDED"
