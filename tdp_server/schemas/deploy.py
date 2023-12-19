from pydantic import BaseModel


class DeployStatus(BaseModel):
    message: str
