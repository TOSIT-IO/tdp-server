from fastapi import APIRouter
from fastapi_pagination.cursor import CursorPage

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.common import StateEnum
from tdp_server.schemas.services import Service, ServiceUpdateResponse
from tdp_server.schemas.variables import Variables

router = APIRouter()


@router.get(
    "",
    response_model=CursorPage[str],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_services():
    """
    Returns a list of services.
    """
    pass


@router.get(
    "/{service_id}",
    response_model=Service,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_service(service_id: str):
    """
    Returns the chosen service details.
    """
    pass


@router.put(
    "/{service_id}",
    response_model=ServiceUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def put_service(service_id: str, options: Service, status: StateEnum):
    """
    Changes the version or status of the service.
    """
    pass


@router.get(
    "/{service_id}/variables",
    response_model=CursorPage[Variables],
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_service_variables(service_id: str):
    """
    Displays the service variables.
    """
    pass


@router.put(
    "/{service_id}/variables",
    response_model=ServiceUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def provide_service_variables(
    service_id: str,
    service: Variables,
):
    """
    Modifies the service variables.
    """
    pass


@router.get(
    "/{service_id}/schema",
    response_model=CursorPage[dict],
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_service_variables(service_id: str):
    """
    Displays the service schema.
    """
    pass
