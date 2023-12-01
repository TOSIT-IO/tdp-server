from typing import List, Optional

from pydantic import BaseModel

from tdp.core.utils import BaseEnum
from tdp_server.schemas.common import ServiceOrComponentUpdateResponse
from tdp_server.schemas.components import Component
from tdp_server.schemas.variables import Variables


class Service(BaseModel):
    id: str
    components: List[Component]
    variables: Optional[Variables] = None
    version: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "hdfs",
                "components": [Component.Config.json_schema_extra["example"]],
                "variables": {
                    "hdfs_site": {"dfs.nameservices": "bigdata_cluster"},
                },
                "version": "ff4627859010bbd6f43808b51121972c0345bbc0",
            }
        }


class ServiceUpdateResponse(ServiceOrComponentUpdateResponse):
    pass


class ServiceStateEnum(BaseEnum):
    RUNNING = "Running"
    STOPPED = "Stopped"
    FAILING = "Failing"


class ServiceStatus(BaseModel):
    service: str
    version: str
    status: ServiceStateEnum
