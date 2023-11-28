from typing import List, Optional

from pydantic import BaseModel

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


class ServiceId(BaseModel):
    id: str


class ServiceUpdateResponse(ServiceOrComponentUpdateResponse):
    pass
