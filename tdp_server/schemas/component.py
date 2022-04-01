from typing import Optional

from pydantic import BaseModel

from tdp_server.schemas.variables import Variables


class Component(BaseModel):
    id: str
    variables: Optional[Variables] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "journalnode",
                "variables": {
                    "hdfs_site": {
                        "dfs.journalnode.kerberos.principal": "jn/master-01.lan@TDP.REALM"
                    }
                },
            }
        }


class ComponentUpdate(BaseModel):
    id: str
    variables: Variables
