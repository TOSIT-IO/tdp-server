from typing import Any, Mapping

from pydantic import BaseModel, RootModel


class Variables(BaseModel):
    RootModel: Mapping[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "hadoop_log_dir": "/var/log/hadoop",
                "yarn_site": {"yarn.http.policy": "HTTPS_ONLY"},
            },
            "description": (
                "A free form object used as a dictionnary in TDP sdk."
                " You can use any kind of data understood as a JSON object"
            ),
        }


class VariableValidation(BaseModel):
    message: str
