import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_pagination.cursor import CursorPage

from tdp.cli import queries
from tdp.cli.session import get_session
from tdp_server.core.config import settings
from tdp_server.api.v1 import dependencies
from tdp_server.schemas.deployments import DeploymentLog
from tdp_server.schemas.operations import OperationLog
from tdp_server.schemas.plan import PlanOperations


router = APIRouter()

logger = logging.getLogger(__name__)

database_dsn = settings.TDP_DATABASE_DSN


@router.get(
    "",
    response_model=CursorPage[DeploymentLog],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployments(limit: int, offset: int):
    """
    Shows list with details of all deployments.
    """
    pass


@router.get(
    "/{deployement_id}",
    response_model=DeploymentLog,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment(deployment_id: int):
    """
    Shows details of a single deployment.
    """
    with get_session(database_dsn, commit_on_exit=True) as session:
        try:
            deployment = queries.get_deployment(session, deployment_id)
            operations1 = [PlanOperations(**o.to_dict()) for o in deployment.operations]
            deployment = DeploymentLog(
                id=deployment.id,
                state=deployment.state,
                deployment_type=deployment.deployment_type,
                start_time=deployment.start_time,
                end_time=deployment.end_time,
                operations=operations1,
                deployment_url="",
                options=deployment.options,
                user="toto",
            )
            logger.info(" GET deployment success.")
            logger.info(type(deployment))
            return deployment

        except Exception as error:
            logger.error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={f"{type(error).__name__}": f"{error}"},
            )


@router.get(
    "/{deployement_id}/operations/{operation_order}",
    response_model=OperationLog,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment_operation(deployment_id, operation_order: str):
    """
    Shows details of a single operation in a deployment.
    """
    with get_session(database_dsn, commit_on_exit=True) as session:
        try:
            deployment_operation = queries.get_operation_order(
                session, deployment_id, operation_order
            )
            logger.info(" GET deployment operation success.")
            return JSONResponse(content=deployment_operation.to_dict())

        except Exception as error:
            logger.error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={f"{type(error).__name__}": f"{error}"},
            )
