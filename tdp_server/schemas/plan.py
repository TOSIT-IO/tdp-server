from pydantic import BaseModel
from typing import Optional, List

from tdp.core.models.state_enum import DeploymentStateEnum, OperationStateEnum
from tdp.core.models.deployment_model import DeploymentTypeEnum


class PlanOperations(BaseModel):
    deployment_id: int
    operation_order: int
    operation: str
    host: Optional[str]
    extra_vars: Optional[List[str]]
    state: OperationStateEnum
    logs: Optional[str]
    options: Optional[dict]


class PlanDag(BaseModel):
    deployment_id: int
    state: Optional[DeploymentStateEnum]
    deployment_type: Optional[DeploymentTypeEnum]
    Operations: List[PlanOperations]
    options: Optional[dict]
