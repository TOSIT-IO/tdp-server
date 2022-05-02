import logging
from typing import Any, Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from tdp.core.dag import Dag

from tdp_server.api import dependencies
from tdp_server.schemas import DeployRequest, DeployStatus
from tdp_server.services.runner import RunnerService, StillRunningException

logger = logging.getLogger("tdp_server")
router = APIRouter()


def check_valid_nodes(nodes: Sequence, dag: Dag):
    difference = set(nodes).difference(dag.components)
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
def deploy_node(
    *,
    deploy_request: DeployRequest = DeployRequest(),
    dag: Dag = Depends(dependencies.get_dag),
    user: str = Depends(dependencies.execute_protected),
    runner_service: RunnerService = Depends(dependencies.get_runner_service),
) -> Any:
    """
    Returns the list of services
    """
    if deploy_request.targets:
        check_valid_nodes(deploy_request.targets, dag)
    if deploy_request.sources:
        check_valid_nodes(deploy_request.sources, dag)

    try:
        runner_service.run_nodes(
            user=user,
            sources=deploy_request.sources,
            targets=deploy_request.targets,
            node_filter=deploy_request.filter,
        )
    except StillRunningException as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="another deployment is still running",
        )
    return {"message": "deployment launched"}


@router.get("/status", response_model=DeployStatus)
def deployment_status(
    runner_service: RunnerService = Depends(dependencies.get_runner_service),
) -> Any:
    if runner_service.running:
        return {"message": "deployment on-going"}
    return {"message": "no deployment on-going"}
