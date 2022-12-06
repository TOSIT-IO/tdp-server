import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from tdp.core.dag import Dag

from tdp_server.api import dependencies
from tdp_server.schemas import DeployRequest, Operation
from tdp_server.services import DeploymentPlanService

logger = logging.getLogger("tdp_server")
router = APIRouter()


@router.post(
    "/dag",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=List[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
async def get_dag_plan(
    *,
    deploy_request: DeployRequest = DeployRequest(),
    dag: Dag = Depends(dependencies.get_dag),
) -> List[Operation]:
    """Returns operations generated by the dag"""
    try:
        deployment_plan = await DeploymentPlanService.from_request(dag, deploy_request)
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return await DeploymentPlanService.get_plan_as_list(deployment_plan)