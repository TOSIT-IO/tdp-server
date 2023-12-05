from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel

from tdp.core.utils import BaseEnum
from tdp_server.schemas.common import ServiceOrComponentUpdateResponse
from tdp_server.schemas.components import Component
from tdp_server.schemas.variables import Variables


class ServiceStateEnum(BaseEnum):
    RUNNING = "Running"
    STOPPED = "Stopped"
    FAILING = "Failing"


class Service(BaseModel):
    id: str
    running_version: str
    configured_version: str
    status: ServiceStateEnum
    components: List[Component]
    variables_url: Optional[Path] = None
    schemas_url: Optional[Path] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "hdfs",
                "running_version": "ff4627859010bbd6f43808b51121972c0345bbc0",
                "configured_version": "ff4627859010bbd6f43808b51121972c0345bbc0",
                "status": "Running",
                "components": [Component.Config.json_schema_extra["example"]],
                "variables_url": "https://...",
                "schema_url": "https://...",
            },
        }


class ServiceUpdateResponse(ServiceOrComponentUpdateResponse):
    pass
