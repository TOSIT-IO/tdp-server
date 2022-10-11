from typing import Generator

from fastapi import Request, Security
from tdp.core.dag import Dag
from tdp.core.runner.operation_runner import OperationRunner
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


def get_dag(request: Request) -> Dag:
    return request.app.state.dag


def get_cluster_variables(request: Request) -> ClusterVariables:
    return request.app.state.cluster_variables


def get_operation_runner(request: Request) -> OperationRunner:
    return request.app.state.operation_runner


def get_runner_service(request: Request) -> RunnerService:
    return request.app.state.runner_service


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
