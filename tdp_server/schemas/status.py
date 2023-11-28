from pydantic import BaseModel


class CurrentStatus(BaseModel):
    service: str
    component: str
    host: str
    running_version: str
    configured_version: str
    to_config: str
    to_restart: str


class StaleComponent(BaseModel):
    service: str
    component: str
    stale: bool
