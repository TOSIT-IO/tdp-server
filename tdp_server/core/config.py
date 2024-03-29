import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, validator
from tdp.core.collection import Collection
from tdp.core.collections import Collections

from tdp_server.core.validator_types import ExistingDir


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    OPENID_CONNECT_DISCOVERY_URL: AnyHttpUrl
    OPENID_CLIENT_ID: str
    OPENID_CLIENT_SECRET: Optional[str] = None

    SCOPE_NAMESPACE: str = "tdp_server"

    PROJECT_NAME: str

    DATABASE_DSN: str

    LOG_LEVEL: str = "INFO"

    @validator("LOG_LEVEL", pre=True)
    def validate_log_level(cls, v: str) -> Any:
        v = v.upper()
        if v in logging._nameToLevel.keys():
            return v
        raise ValueError(v)

    TDP_COLLECTION_PATH: str
    TDP_RUN_DIRECTORY: ExistingDir
    TDP_VARS: ExistingDir

    TDP_COLLECTIONS: Collections = Collections({})

    @validator("TDP_COLLECTIONS", pre=True)
    def collections_factory(
        cls, v: Optional[List[Collection]], values: Dict[str, Any]
    ) -> Any:
        tdp_collection_path = values.get("TDP_COLLECTION_PATH", "")
        if not tdp_collection_path:
            raise ValueError("tdp_collection_path is empty")
        return Collections.from_collection_list(
            [
                Collection.from_path(path)
                for path in tdp_collection_path.split(os.pathsep)
            ]
        )

    DO_NOT_USE_IN_PRODUCTION_DISABLE_TOKEN_CHECK: bool = False

    MOCK_DEPLOY: bool = False

    class Config:
        case_sensitive = True
        env_file = ".env"


class TestSettings(Settings):
    SERVER_NAME = "localhost"
    SERVER_HOST = AnyHttpUrl("http://localhost", scheme="http")
    OPENID_CONNECT_DISCOVERY_URL = AnyHttpUrl("http://localhost", scheme="http")
    OPENID_CLIENT_ID = ""
    PROJECT_NAME = "test-tdp-server"
    DATABASE_DSN = "sqlite://"
    TDP_COLLECTION_PATH = "."
    TDP_COLLECTIONS: Collections = Collections({})
    TDP_RUN_DIRECTORY: Path = Path(".none/")
    TDP_VARS: Path = Path(".none/")


if "pytest" in sys.modules:
    settings = TestSettings.construct()
else:
    settings = Settings()  # type: ignore
