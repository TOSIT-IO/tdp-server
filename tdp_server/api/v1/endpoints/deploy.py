from fastapi import APIRouter

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.deployments import DeploymentLog
from tdp_server.schemas.operations import OperationLog
from tdp_server.schemas.deploy import DeployOptions


router = APIRouter()


@router.post(
    "/deploy",
    response_model=DeploymentLog,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMMON_DEPLOYMENT_ARGS,
    },
)
def post_deploy(options: DeployOptions):
    pass
