import logging

from fastapi import APIRouter, Depends
from tdp.core.variables import ClusterVariables, ServiceVariables

from tdp_server.api import dependencies

logger = logging.getLogger("tdp_server")
router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=dict,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_schemas(
    *, cluster_variables: ClusterVariables = Depends(dependencies.get_cluster_variables)
):
    return {name: service.schema for name, service in cluster_variables.items()}


@router.get(
    "/{service_id}",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=dict,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_schema(*, service: ServiceVariables = Depends(dependencies.service)):
    return service.schema
