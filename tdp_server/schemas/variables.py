from typing import Any, Mapping

from pydantic import BaseModel


class Variables(BaseModel):
    __root__: Mapping[str, Any]

    class Config:
        schema_extra = {
            "example": {
                "hadoop_log_dir": "/var/log/hadoop",
                "yarn_site": {"yarn.http.policy": "HTTPS_ONLY"},
            },
            "description": (
                "A free form object used as a dictionnary in TDP sdk."
                " You can use any kind of data understood as a JSON object"
            ),
        }
