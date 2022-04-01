from pydantic import BaseModel


class DeployStatus(BaseModel):
    message: str

    class Config:
        json_schema_extra = {"example": {"message": "Deployment successful"}}
