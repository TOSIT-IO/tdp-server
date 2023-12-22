from datetime import datetime
from pydantic import BaseModel
from typing import List

from tdp_server.schemas.common import ServiceOrComponentUpdateResponse
from tdp_server.schemas.status import CurrentStatus


class Component(BaseModel):
    id: str
    service_id: str
    variables_url: str
    running_version: str
    configured_version: str
    to_config: bool
    to_restart: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id": "journalnode",
                "service_id": "hdfs",
                "running_version": "ff4627859010bbd6f43808b51121972c0345bbc0",
                "configured_version": "ff4627859010bbd6f43808b51121972c0345bbc0",
                "variables_url": "https://...",
                "to_config": False,
                "to_restart": False,
            }
        }


class Components(BaseModel):
    service_id: str
    components: List[Component]

    class config:
        json_schema_extra = {
            "example": {
                "service_id": "hdfs",
                "components": [Component.Config.json_schema_extra["example"]],
            }
        }


class StatusHistory(CurrentStatus):
    id: int
    source: str
    deployment_id: int
    event_time: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "component": "journalnode",
                "service_id": "hdfs",
                "running_version": "ff4627859010bbd6f43808b51121972c0345bbc0",
                "configured_version": "ff4627859010bbd6f43808b51121972c0345bbc0",
                "host": "master-01",
                "to_config": False,
                "to_restart": True,
                "id": 1,
                "service_id": "hdfs",
                "deployment_id": 1,
                "event_time": "2023-12-21 12:34:54",
            }
        }


class ComponentUpdateResponse(ServiceOrComponentUpdateResponse):
    pass
