from typing import List, Mapping, Union

from pydantic import BaseModel

SCALAR_TYPE = Union[str, int, float, bool, None]


class Variables(BaseModel):
    __root__: Mapping[
        str, Union[SCALAR_TYPE, List[SCALAR_TYPE], Mapping[str, SCALAR_TYPE]]
    ]

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
