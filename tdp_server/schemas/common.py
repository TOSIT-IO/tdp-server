from pydantic import BaseModel


class ServiceOrComponentUpdateResponse(BaseModel):
    message: str

    class Config:
        json_schema_extra = {"example": {"message": "Update successful"}}
