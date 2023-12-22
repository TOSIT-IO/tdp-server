from pydantic import BaseModel


class CurrentStatus(BaseModel):
    service: str
    component: str
    host: str
    running_version: str
    configured_version: str
    to_config: bool
    to_restart: bool

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
            }
        }
