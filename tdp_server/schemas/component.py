from typing import Optional

from pydantic import BaseModel

from tdp_server.schemas.common import (
    ServiceOrComponentUpdate,
    ServiceOrComponentUpdateResponse,
)
from tdp_server.schemas.variables import Variables


class Component(BaseModel):
    id: str
    service_id: str
    variables: Optional[Variables] = None
    version: str

    class Config:
        schema_extra = {
            "example": {
                "id": "journalnode",
                "version": "ff4627859010bbd6f43808b51121972c0345bbc0",
                "variables": {
                    "hdfs_site": {
                        "dfs.journalnode.kerberos.principal": "jn/master-01.lan@TDP.REALM"
                    }
                },
            }
        }


class ComponentUpdate(ServiceOrComponentUpdate):
    pass


class ComponentUpdateResponse(ServiceOrComponentUpdateResponse):
    pass
