from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel

from tdp_server.schemas.common import ServiceOrComponentUpdateResponse


class Service(BaseModel):
    id: str
    service_url: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "hdfs",
                "service_url": "http://.../api/v1/services/hdfs",
            }
        }


class ServiceConf(BaseModel):
    id: str
    running_version: str
    configured_version: str
    variables_url: Optional[Path] = None
    schemas_url: Optional[Path] = None


class ServiceUpdateResponse(ServiceOrComponentUpdateResponse):
    pass
