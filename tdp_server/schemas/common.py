from pydantic import BaseModel
from typing import Optional, List


class ServiceOrComponentUpdateResponse(BaseModel):
    message: str

    class Config:
        json_schema_extra = {"example": {"message": "Update successful"}}
