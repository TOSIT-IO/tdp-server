# from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

# from logging.config import dictConfig
# from tdp_server.log_config import logging_config, logger

from tdp_server.api.v1 import dependencies
from tdp_server.core.config import settings, collections
from tdp_server.schemas.deploy import DeploymentStart

from tdp.cli.queries import (
    get_planned_deployment,
    get_sch_status,
)
from tdp.cli.session import get_session
from tdp.cli.utils import check_services_cleanliness, print_deployment
from tdp.core.cluster_status import ClusterStatus
from tdp.core.deployment import DeploymentRunner, Executor
from tdp.core.models import DeploymentStateEnum, DeploymentModel
from tdp.core.variables import ClusterVariables


router = APIRouter()

# dictConfig(logging_config)

logger = logging.getLogger("tdp_server_logger.deploy")

database_dsn = settings.TDP_DATABASE_DSN


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
            message = "No planned deployment found, please run `tdp plan` first."
            logger.error(message)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
            )
        try:
            deployment_iterator = DeploymentRunner(
                collections=collections,
                executor=Executor(
                    run_directory=run_directory.absolute() if run_directory else None,
                    dry=dry or mock_deploy,
                ),
                cluster_variables=cluster_variables,
                cluster_status=ClusterStatus.from_sch_status_rows(
                    get_sch_status(session)
                ),
            ).run(planned_deployment, force_stale_update=force_stale_update)

            if dry:
                for _ in deployment_iterator:
                    pass
                output = "Deployment successfuly executed in dry mode"
                logger.info(output)
                return output

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
            logger.info(message)
            return message
        except Exception as error:
            logger.error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={f"{type(error).__name__}": f"{error}"},
            )


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
        try:
            deployment = (
                session.query(DeploymentModel)
                .where(DeploymentModel.state == "Running")
                .order_by(DeploymentModel.id.desc())
                .limit(1)
                .one()
            )
            if deployment:
                operations1 = [o.to_dict() for o in deployment.operations]
                output = {
                    "deployment_id": deployment.id,
                    "state": deployment.state,
                    "deployment_type": deployment.deployment_type,
                    "operations": operations1,
                    "options": deployment.options,
                }
                return JSONResponse(output)
        except Exception as error:
            logger.error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={f"{type(error).__name__}": f"{error}"},
            )
