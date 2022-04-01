from typing import List, Optional

from pydantic import BaseModel

from tdp_server.schemas.component import Component, ComponentUpdate
from tdp_server.schemas.variables import Variables


class Service(BaseModel):
    id: str
    components: List[Component]
    variables: Optional[Variables] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "hdfs",
                "components": [Component.Config.schema_extra["example"]],
                "variables": {
                    "hdfs_site": {"dfs.nameservices": "bigdata_cluster"},
                },
            }
        }


class ServiceUpdate(BaseModel):
    message: str
    variables: Variables


class ServiceUpdateResponse(BaseModel):
    message: str
    version: str
