from fastapi import APIRouter
from pathlib import Path

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.deployments import DeploymentLog


router = APIRouter()


@router.post(
    "",
    response_model=DeploymentLog,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMMON_DEPLOYMENT_ARGS,
    },
)
def deploy(
    force_stale_update: bool = False,
    dry: bool = False,
    mock_deploy: bool = False,
    validate: bool = True,
):
    """
    Deploys the planned dag/operations.

    Options:

        - force_stale_update: Force stale status update.

        - dry: Execute the dag without running any actions.

        - mock_deploy: Mock the deploy, do not actually run the ansible playbook.

        - validate: validates service variables.
    """
    pass


@router.get(
    "",
    response_model=DeploymentLog,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment_status():
    """
    Shows last deployment's deploymentlog.
    """
    pass
