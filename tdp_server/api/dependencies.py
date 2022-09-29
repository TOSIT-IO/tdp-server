from functools import lru_cache
from typing import Dict, Generator

from fastapi import Depends, Security
from tdp.core.dag import Dag
from tdp.core.variables import ClusterVariables

from tdp_server.api.openid_dependencies import validate_token
from tdp_server.core.config import settings
from tdp_server.db.session import SessionLocal
from tdp_server.services import RunnerService

COMMON_RESPONSES = {
    401: {
        "description": "Unauthenticated",
        "content": {
            "application/json": {
                "example": {"detail": "Error during authentication validation (reason)"}
            }
        },
    },
    403: {
        "description": "Not enough privileges",
        "headers": {
            "WWW-Authenticate": {
                "schema": {"type": "string"},
                "description": "Authentication method to use",
            }
        },
        "content": {
            "application/json": {"example": {"detail": "Not enough permissions"}}
        },
    },
}


def get_db() -> Generator:
    with SessionLocal() as db:
        yield db


@lru_cache()
def get_dag() -> Dag:
    return Dag(settings.TDP_COLLECTIONS)


@lru_cache()
def get_cluster_variables() -> ClusterVariables:
    return ClusterVariables.get_cluster_variables(settings.TDP_VARS)


@lru_cache()
def get_runner_service(dag: Dag = Depends(get_dag)) -> RunnerService:
    return RunnerService(
        dag,
        settings.TDP_RUN_DIRECTORY,
        settings.TDP_VARS,
    )


async def read_protected(
    user_info=Security(validate_token, scopes=[settings.SCOPE_NAMESPACE + ":read"])
) -> str:
    return user_info["sub"]


async def write_protected(
    user_info=Security(validate_token, scopes=[settings.SCOPE_NAMESPACE + ":write"])
) -> str:
    return user_info["sub"]


async def execute_protected(
    user_info=Security(validate_token, scopes=[settings.SCOPE_NAMESPACE + ":execute"])
) -> str:
    return user_info["sub"]
