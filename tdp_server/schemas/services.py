from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel

from tdp_server.schemas.common import ServiceOrComponentUpdateResponse


class Service(BaseModel):
    id: str
    service_url: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "hdfs",
                "service_url": "http://localhost/api/v1/services/hdfs",
            }
        }


class ServiceConf(BaseModel):
    id: str
    running_version: str
    configured_version: str
    to_config: bool
    to_restart: bool
    variables_url: Optional[Path] = None
    schemas_url: Optional[Path] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "spark3",
                "running_version": "5b67589",
                "configured_version": "5b67589",
                "to_config": "False",
                "to_restart": "False",
                "variables_url": "http://localhost/api/v1/services/spark3/variables",
                "schemas_url": "http://localhost/api/v1/services/spark3/schema",
            }
        }


class ServiceSchema(BaseModel):
    service_schema: dict

    class Config:
        json_schema_extra = {
            "example": {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "TOSIT-IO/tdp/schema/hadoop.json",
                "title": "HADOOP",
                "description": "TDP's HADOOP configuration variables",
                "type": "object",
                "properties": {
                    "hadoop_release": {
                        "description": "Hadoop's release version",
                        "type": "string",
                    },
                    "hadoop_dist_file": {
                        "description": "Hadoop's release archive name, left to default, it will use `hadoop_release` to construct the archive name",
                        "type": "string",
                        "default": "{{ hadoop_release }}.tar.gz",
                    },
                },
                "required": ["hadoop_release", "hadoop_dist_file"],
            }
        }


class ServiceUpdateResponse(ServiceOrComponentUpdateResponse):
    pass
