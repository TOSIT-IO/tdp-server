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
def deploy(options: DeployOptions):
    """
    Deploys the planned dag/operations.

    Options:

        - force_stale_update: Force stale status update.

        - dry: Execute the dag without running any actions.

        - mock_deploy: Mock the deploy, do not actually run the ansible playbook.

        - run_directory: Working directory where the executor is launched (`ansible-playbook` for Ansible).

        - validate: validates service variables.

        - collection: Path to the collections.

        - database_dsn: Database Data Square Name, in sqlalchemy driver for example: sqlite:////data/tdp.db.

        - vars: Path to the TDP variables.
    """
    pass
