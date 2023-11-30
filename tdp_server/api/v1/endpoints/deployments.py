from fastapi import APIRouter
from typing import List

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
    response_model=List[DeploymentLog],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployments():
    pass


@router.get(
    "/{deployement_id}",
    response_model=DeploymentLogWithOperations,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment():
    pass


@router.get(
    "/{deployement_id}/operation/{operation}",
    response_model=OperationLog,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment_operation():
    pass


@router.get(
    "/status",
    response_model=DeployStatus,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment_status():
    pass


@router.post(
    "/dag",
    response_model=DeploymentLog,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMMON_DEPLOYMENT_ARGS,
    },
)
def post_dag():
    pass


@router.post(
    "/operations",
    response_model=DeploymentLog,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMMON_DEPLOYMENT_ARGS,
    },
)
def post_operations():
    pass


@router.post(
    "/resume",
    response_model=DeploymentLog,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMMON_DEPLOYMENT_ARGS,
    },
)
def post_resume():
    pass


@router.post(
    "/reconfigure",
    response_model=DeploymentLog,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMMON_DEPLOYMENT_ARGS,
    },
)
def post_reconfigure():
    pass
