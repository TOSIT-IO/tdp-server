from typing import List, Optional

from pydantic import BaseModel


class DeployRequest(BaseModel):
    targets: Optional[List[str]] = []
    filter: Optional[str] = None
    sources: Optional[List[str]] = []


class DeployStatus(BaseModel):
    message: str
