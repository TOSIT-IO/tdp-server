import logging
from typing import Any, List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from tdp.core.collections import Collections
from tdp.core.dag import Dag
from tdp.core.runner import DeploymentPlan
from tdp.core.variables import ClusterVariables

from tdp_server.api import dependencies
from tdp_server.db.session import SessionLocal
from tdp_server.schemas import (
    DeploymentLog,
    DeploymentLogWithOperations,
    DeployRequest,
    DeployStatus,
    OperationLog,
    ResumeRequest,
    RunRequest,
)
from tdp_server.services import (
    DeploymentCrud,
    DeploymentPlanService,
    RunnerService,
    StillRunningException,
)

logger = logging.getLogger("tdp_server")
router = APIRouter()


async def launch_deployment(
    runner_service: RunnerService,
    background_tasks: BackgroundTasks,
    user: str,
    deployment_plan: DeploymentPlan,
) -> DeploymentLog:
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


COMMON_DEPLOYMENT_ARGS = {
    "responses": {
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
    "status_code": status.HTTP_202_ACCEPTED,
}


@router.post("/", **COMMON_DEPLOYMENT_ARGS)
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

    try:
        deployment_plan = await DeploymentPlanService.from_request(dag, deploy_request)
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return await launch_deployment(
        runner_service, background_tasks, user, deployment_plan
    )


@router.post("/run", **COMMON_DEPLOYMENT_ARGS)
async def run_nodes(
    *,
    run_request: RunRequest,
    collections: Collections = Depends(dependencies.get_collections),
    user: str = Depends(dependencies.execute_protected),
    runner_service: RunnerService = Depends(dependencies.get_runner_service),
    background_tasks: BackgroundTasks,
):
    try:
        deployment_plan = await DeploymentPlanService.from_run_request(
            collections, run_request
        )
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return await launch_deployment(
        runner_service,
        background_tasks,
        user,
        deployment_plan,
    )


@router.post("/resume", **COMMON_DEPLOYMENT_ARGS)
async def resume(
    *,
    resume_request: ResumeRequest = ResumeRequest(),
    db: Session = Depends(dependencies.get_db),
    dag: Dag = Depends(dependencies.get_dag),
    user: str = Depends(dependencies.execute_protected),
    runner_service: RunnerService = Depends(dependencies.get_runner_service),
    background_tasks: BackgroundTasks,
):
    try:
        deployment_plan = await DeploymentPlanService.from_resume_request(
            db, dag, resume_request
        )
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return await launch_deployment(
        runner_service,
        background_tasks,
        user,
        deployment_plan,
    )


@router.post("/reconfigure", **COMMON_DEPLOYMENT_ARGS)
async def reconfigure(
    *,
    db: Session = Depends(dependencies.get_db),
    dag: Dag = Depends(dependencies.get_dag),
    cluster_variables: ClusterVariables = Depends(dependencies.get_cluster_variables),
    user: str = Depends(dependencies.execute_protected),
    runner_service: RunnerService = Depends(dependencies.get_runner_service),
    background_tasks: BackgroundTasks,
):
    try:
        deployment_plan = await DeploymentPlanService.from_reconfigure_request(
            db, dag, cluster_variables
        )
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return await launch_deployment(
        runner_service,
        background_tasks,
        user,
        deployment_plan,
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
