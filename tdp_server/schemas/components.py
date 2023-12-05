from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from tdp_server.schemas.common import ServiceOrComponentUpdateResponse
from tdp_server.schemas.status import CurrentStatus
from tdp_server.schemas.variables import Variables


class Component(BaseModel):
    id: str
    service_id: str
    variables: Optional[Variables] = None
    running_version: str
    configured_version: str
    host: str
    to_config: str
    to_restart: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "journalnode",
                "running_version": "ff4627859010bbd6f43808b51121972c0345bbc0",
                "configured_version": "ff4627859010bbd6f43808b51121972c0345bbc0",
                "host": "master-01",
                "variables": {
                    "hdfs_site": {
                        "dfs.journalnode.kerberos.principal": "jn/master-01.lan@TDP.REALM"
                    }
                },
            }
        }


class StatusHistory(CurrentStatus):
    id: int
    source: str
    deployment_id: int
    event_time: datetime


class StaleComponent(BaseModel):
    service: str
    component: str
    stale: bool


class ComponentUpdateResponse(ServiceOrComponentUpdateResponse):
    pass
