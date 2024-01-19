from pydantic import BaseModel, validator
from typing import Optional, List, Union

from tdp.core.models.state_enum import DeploymentStateEnum, OperationStateEnum
from tdp.core.models.deployment_model import DeploymentTypeEnum


class PlanOperations(BaseModel):
    deployment_id: Union[int, None]
    operation_order: int
    operation: str
    host: Union[str, None]
    extra_vars: Union[List[str], None]
    state: Union[DeploymentStateEnum, str]
    logs: Union[str, None]

    def __init__(self, **data):
        data["deployment_id"] = data.get("deployment_id", None) or None
        data["extra_vars"] = data.get("extra_vars", []) or None
        super().__init__(**data)


class PlanDag(BaseModel):
    deployment_id: Union[int, None]
    state: Union[DeploymentStateEnum, None]
    deployment_type: Union[DeploymentTypeEnum, None]
    operations: Union[List[PlanOperations], None]
    options: Union[dict, None]
