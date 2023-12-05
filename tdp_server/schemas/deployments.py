from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from tdp.core.models.state_enum import DeploymentStateEnum
from tdp.core.models.deployment_model import DeploymentTypeEnum
from tdp_server.schemas.operations import OperationLog


class ResumeRequest(BaseModel):
    id: Optional[int] = Field(
        default=None,
        title="Deployment ID",
        description="Deployment ID to resume from. (must be a failed deployment)",
    )


class DeployStatus(BaseModel):
    message: str


class DeploymentLog(BaseModel):
    id: int
    options: Optional[dict]
    start_time: datetime
    end_time: Optional[datetime] = None
    restart: bool = False
    status: DeploymentStateEnum
    deployment_type: DeploymentTypeEnum
    operations: List[str]
    user: Optional[str] = "NO_USER_RECORDED"


class DeploymentLogWithOperations(DeploymentLog):
    operations: List[OperationLog]
