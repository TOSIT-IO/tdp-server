from __future__ import annotations
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from tdp_server.api.v1 import dependencies
from tdp_server.core.config import settings, collections
from tdp_server.schemas.deploy import DeploymentStart

from tdp.cli.queries import (
    get_deployments,
    get_planned_deployment,
    get_sch_status,
)
from tdp.cli.session import get_session
from tdp.cli.utils import check_services_cleanliness, print_deployment
from tdp.core.cluster_status import ClusterStatus
from tdp.core.collections import Collections
from tdp.core.deployment import DeploymentRunner, Executor
from tdp.core.models import DeploymentStateEnum
from tdp.core.variables import ClusterVariables


router = APIRouter()

database_dsn = settings.TDP_DATABASE_DSN


@router.post(
    "",
    # response_model=DeploymentStart,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMMON_DEPLOYMENT_ARGS,
    },
)
def deploy_f(
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

    run_directory = settings.TDP_RUN_DIRECTORY
    vars = settings.TDP_VARS

    cluster_variables = ClusterVariables.get_cluster_variables(
        collections, vars, validate=validate
    )
    check_services_cleanliness(cluster_variables)

    with get_session(database_dsn, commit_on_exit=True) as session:
        planned_deployment = get_planned_deployment(session)
        if planned_deployment is None:
            return "No planned deployment found, please run `tdp plan` first."

        deployment_iterator = DeploymentRunner(
            collections=collections,
            executor=Executor(
                run_directory=run_directory.absolute() if run_directory else None,
                dry=dry or mock_deploy,
            ),
            cluster_variables=cluster_variables,
            cluster_status=ClusterStatus.from_sch_status_rows(get_sch_status(session)),
        ).run(planned_deployment, force_stale_update=force_stale_update)

        if dry:
            for _ in deployment_iterator:
                pass
            return "Deployment successfuly executed in dry mode"

        # deployment and operations records are mutated by the iterator so we need to
        # commit them before iterating and at each iteration
        session.commit()  # Update deployment status to RUNNING, operations to PENDING
        for cluster_status_logs in deployment_iterator:
            session.commit()  # Update operation status to RUNNING
            if cluster_status_logs and any(cluster_status_logs):
                session.add_all(cluster_status_logs)
            session.commit()  # Update operation status to SUCCESS, FAILURE or HELD

        if deployment_iterator.deployment.state != DeploymentStateEnum.SUCCESS:
            message = "Deployment failed."
        else:
            message = "Deployment finished with success."

    return message


@router.get(
    "",
    response_model=DeploymentStart,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment_status():
    """
    Shows the current deployment's DeploymentLog.
    """

    with get_session(database_dsn) as session:
        deployment = get_deployments(session, limit=1, offset=0)
        if deployment:
            operations = [o.to_dict() for o in deployment[0].operations]

            return JSONResponse(operations)
