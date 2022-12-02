from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator
from tdp.core.models import FilterTypeEnum, StateEnum

from tdp_server.schemas.operation import OperationLog


class DeployRequest(BaseModel):
    targets: Optional[List[str]] = Field(
        default=None,
        title="Deployment Targets",
        description="List of operations used as targets on the dag generation, mutually exclusive with `sources`.",
    )
    sources: Optional[List[str]] = Field(
        default=None,
        title="Deployment Sources",
        description="List of operations used as sources on the dag generation, mutually exclusive with `targets`.",
    )
    filter_type: Optional[FilterTypeEnum] = Field(
        default=None,
        title="Deployment Sources",
        description="Controls how the filter expression must be interpreted.",
    )
    filter_expression: Optional[str] = Field(
        default=None,
        title="Filter Expression",
        description=(
            "Expression which will match on the operation list generated from the dag. "
            "Only operations matching will be kept for the deployment."
        ),
    )
    restart: bool = Field(
        default=False,
        title="Replace starts",
        description="Controls whether or not start operations will be replaced by a restart operation.",
    )

    @validator("sources")
    def sources_validator(cls, value, values):
        if value is not None and values.get("targets") is not None:
            raise ValueError("targets and sources fields are mutually exclusive")
        return value


class DeployStatus(BaseModel):
    message: str


class Deployment(BaseModel):
    id: int
    sources: Optional[List[str]] = None
    targets: Optional[List[str]] = None
    filter_expression: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    restart: bool = False
    state: StateEnum
    operations: List[str]
    user: str


class DeploymentWithOperations(Deployment):
    operations: List[OperationLog]
