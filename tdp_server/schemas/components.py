from pydantic import BaseModel
from typing import List

from tdp_server.schemas.common import ServiceOrComponentUpdateResponse
from tdp_server.schemas.configuration import CurrentStatus


class Component(BaseModel):
    id: str
    variables_url: str
    running_version: str
    configured_version: str
    to_config: bool
    to_restart: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id": "journalnode",
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


class ComponentUpdateResponse(ServiceOrComponentUpdateResponse):
    pass
