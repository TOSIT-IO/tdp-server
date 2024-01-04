from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from tdp.core.utils import BaseEnum
from tdp.core.models.state_enum import DeploymentStateEnum


class Operationtype(BaseEnum):
    DAG = "DAG"
    OTHER = "OTHER"


class Operation(BaseModel):
    operation: str
    hosts: Optional[set[str]]

    class Config:
        json_schema_extra = {
            "example": {
                "operation": "hbase_master_config",
                "hosts": ["master-01", "master-02"],
            }
        }


class OperationLog(BaseModel):
    operation: str
    start_time: datetime
    end_time: datetime
    status: DeploymentStateEnum
    logs: bytes
