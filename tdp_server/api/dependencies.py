from typing import Generator

from fastapi import Depends, HTTPException, Path, Request, Security, status
from tdp.core.collections import Collections
from tdp.core.dag import Dag
from tdp.core.deployment import DeploymentRunner
from tdp.core.variables import ClusterVariables, ServiceVariables

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

SERVICE_ID_DOES_NOT_EXIST_ERROR = {
    400: {
        "description": "Service id does not exists",
        "content": {
            "application/json": {"example": {"detail": "{service_id} does not exists"}}
        },
    }
}

COMPONENT_ID_DOES_NOT_EXIST_ERROR = {
    400: {
        "description": "Component id does not exists",
        "content": {
            "application/json": {
                "example": {"detail": "{component_id} does not exists"}
            }
        },
    }
}


def get_db() -> Generator:
    with SessionLocal() as db:
        yield db


def get_dag(request: Request) -> Dag:
    return request.app.state.dag


def get_cluster_variables(request: Request) -> ClusterVariables:
    return request.app.state.cluster_variables


def get_deployment_runner(request: Request) -> DeploymentRunner:
    return request.app.state.deployment_runner


def get_collections(request: Request) -> Collections:
    return request.app.state.settings.TDP_COLLECTIONS


def get_runner_service(request: Request) -> RunnerService:
    return request.app.state.runner_service


def service(
    service_id: str = Path(),
    cluster_variables: ClusterVariables = Depends(get_cluster_variables),
) -> ServiceVariables:
    service_id = service_id.lower()
    service_variables = cluster_variables.get(service_id)
    if service_variables is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{service_id} does not exist.",
        )
    return service_variables


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
