from datetime import datetime
from pydantic import BaseModel

from tdp_server.schemas.common import ServiceOrComponentUpdateResponse
from tdp_server.schemas.status import CurrentStatus


class Component(BaseModel):
    id: str
    service_id: str
    variables_url: str
    running_version: str
    configured_version: str
    to_config: str
    to_restart: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "journalnode",
                "service_id": "hdfs",
                "running_version": "ff4627859010bbd6f43808b51121972c0345bbc0",
                "configured_version": "ff4627859010bbd6f43808b51121972c0345bbc0",
                "host": "master-01",
                "variables_url": "https://...",
            }
        }


class StatusHistory(CurrentStatus):
    id: int
    source: str
    deployment_id: int
    event_time: datetime


class ComponentUpdateResponse(ServiceOrComponentUpdateResponse):
    pass
