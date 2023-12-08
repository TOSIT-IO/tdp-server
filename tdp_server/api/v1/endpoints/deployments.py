from fastapi import APIRouter
from fastapi_pagination.cursor import CursorPage

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
    response_model=CursorPage[DeploymentLog],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployments():
    """
    Shows list with details of all deployments.
    """
    pass


@router.get(
    "/{deployement_id}",
    response_model=DeploymentLogWithOperations,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment(deployement_id: int):
    """
    Shows details of a single deployment.
    """
    pass


@router.get(
    "/{deployement_id}/operations/{operation_order}/logs",
    response_model=OperationLog,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment_operation(deployement_id: int, operation_order: str):
    """
    Shows details of a single operation in a deployment.
    """
    pass


@router.get(
    "/status",
    response_model=DeployStatus,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment_status():
    """
    Shows if the last deployment was successful.
    """
    pass
