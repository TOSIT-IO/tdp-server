from fastapi import APIRouter
from pathlib import Path

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.deployments import DeploymentLog
from tdp_server.schemas.operations import OperationLog


router = APIRouter()


@router.post(
    "/deploy",
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
    vars: Path = None,
):
    """
    Deploys the planned dag/operations.

    Options:

        - force_stale_update: Force stale status update.

        - dry: Execute the dag without running any actions.

        - mock_deploy: Mock the deploy, do not actually run the ansible playbook.

        - validate: validates service variables.

        - vars: Path to the TDP variables.
    """
    pass
