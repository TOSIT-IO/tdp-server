from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel

from tdp.core.utils import BaseEnum
from tdp_server.schemas.common import ServiceOrComponentUpdateResponse


class ServiceStateEnum(BaseEnum):
    RUNNING = "Running"
    STOPPED = "Stopped"
    FAILING = "Failing"


class Service(BaseModel):
    id: str
    running_version: str
    configured_version: str
    status: ServiceStateEnum
    variables_url: Optional[Path] = None
    schemas_url: Optional[Path] = None


class ServiceUpdateResponse(ServiceOrComponentUpdateResponse):
    pass
