from pydantic import BaseModel
from typing import Optional, List


class PlanOptionsCommon(BaseModel):
    preview: bool
    collections: List[str]
    database_dsn: str


class PlanOptionsDag(PlanOptionsCommon):
    source: tuple[str]
    target: tuple[str]
    restart: bool
    reverse: bool
    stop: bool
    filter: Optional[str] = None


class PlanOptionsReconfigure(PlanOptionsCommon):
    rolling_interval: Optional[int] = None


class PlanOptionsOperations(PlanOptionsReconfigure):
    operation_names: tuple[str]
    extra_vars: tuple[str]
    hosts: tuple[str]


class PlanOptionsCostum(PlanOptionsOperations, PlanOptionsDag):
    pass
