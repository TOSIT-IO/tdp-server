from fastapi import APIRouter

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.deploy import DeploymentStart


router = APIRouter()


@router.post(
    "",
    response_model=str,
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
    raise NotImplementedError


@router.get(
    "",
    response_model=DeploymentStart,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment_status():
    """
    Shows the current deployment's DeploymentLog.
    """
    raise NotImplementedError
