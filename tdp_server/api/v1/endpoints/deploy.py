import logging
from typing import Any, List, Optional, Sequence

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from tdp.core.dag import Dag

from tdp_server.api import dependencies
from tdp_server.db.session import SessionLocal
from tdp_server.schemas import (
    DeploymentLog,
    DeploymentLogWithOperations,
    DeployRequest,
    DeployStatus,
    OperationLog,
)
from tdp_server.services import DeploymentCrud, RunnerService, StillRunningException

logger = logging.getLogger("tdp_server")
router = APIRouter()


def check_valid_nodes(nodes: Sequence, dag: Dag):
    difference = set(nodes).difference(dag.operations)
    if difference:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"the following nodes do not exist: {','.join(difference)}",
        )


@router.post(
    "/",
    responses={
        **dependencies.COMMON_RESPONSES,
        409: {
            "description": "Another deployment is still running, only one deployment at a time is allowed",
            "content": {
                "application/json": {
                    "example": {"detail": "another deployment is still running"}
                }
            },
        },
    },
    status_code=status.HTTP_202_ACCEPTED,
)
async def deploy_node(
    *,
    deploy_request: DeployRequest = DeployRequest(),
    dag: Dag = Depends(dependencies.get_dag),
    user: str = Depends(dependencies.execute_protected),
    runner_service: RunnerService = Depends(dependencies.get_runner_service),
    background_tasks: BackgroundTasks,
) -> DeploymentLog:
    """
    Launches a deployment from the dag
    """
    if deploy_request.targets:
        check_valid_nodes(deploy_request.targets, dag)
    if deploy_request.sources:
        check_valid_nodes(deploy_request.sources, dag)

    try:
        deployment_plan = await runner_service.make_deployment_plan(dag, deploy_request)
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    try:
        return await runner_service.run(
            background_tasks=background_tasks,
            session_local=SessionLocal,
            user=user,
            deployment_plan=deployment_plan,
        )

    except StillRunningException as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="another deployment is still running",
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="check server logs to investigate error",
        )


@router.get(
    "/status",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=DeployStatus,
)
def deployment_status(
    runner_service: RunnerService = Depends(dependencies.get_runner_service),
) -> Any:
    if runner_service.running:
        return {"message": "deployment on-going"}
    return {"message": "no deployment on-going"}


@router.get(
    "/",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=List[DeploymentLog],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployments(
    *,
    limit: int = 15,
    offset: int = 0,
    db: Session = Depends(dependencies.get_db),
):
    return DeploymentCrud.get_deployments(db, limit, offset)


@router.get(
    "/{deployment_id}",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=DeploymentLogWithOperations,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment(
    *,
    deployment_id: int,
    db: Session = Depends(dependencies.get_db),
):
    try:
        return DeploymentCrud.get_deployment(db, deployment_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deployment not found",
        )


@router.get(
    "/{deployment_id}/operation/{operation}",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=OperationLog,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_deployment_operation(
    *,
    deployment_id: int,
    operation: str,
    db: Session = Depends(dependencies.get_db),
):
    try:
        return DeploymentCrud.get_deployment_operation(db, deployment_id, operation)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deployment or operation not found",
        )
