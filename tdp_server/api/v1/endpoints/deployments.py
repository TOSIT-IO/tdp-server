from fastapi import APIRouter
from fastapi_pagination import Page

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.deployments import (
    DeploymentLog,
    DeploymentLogWithOperations,
    DeployStatus,
)
from tdp_server.schemas.operations import OperationLog


router = APIRouter()


@router.get(
    "/",
    response_model=Page[DeploymentLog],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployments():
    pass


@router.get(
    "/{deployement_id}",
    response_model=DeploymentLogWithOperations,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment(deployement_id: int):
    pass


@router.get(
    "/{deployement_id}/operations/{operation_order}/logs",
    response_model=OperationLog,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment_operation(deployement_id: int, operation_order: str):
    pass


@router.get(
    "/status",
    response_model=DeployStatus,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment_status():
    pass
