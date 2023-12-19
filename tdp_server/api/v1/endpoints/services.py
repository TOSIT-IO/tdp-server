from fastapi import APIRouter
from fastapi_pagination.cursor import CursorPage

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.services import Service, ServiceConf, ServiceUpdateResponse
from tdp_server.schemas.variables import Variables

router = APIRouter()


@router.get(
    "",
    response_model=CursorPage[Service],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_services():
    """
    Returns a list of services.
    """
    pass


@router.get(
    "/{service_id}",
    response_model=ServiceConf,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_service(service_id: str, to_config, to_restart):
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
def put_service(
    service_id: str,
    to_config: bool,
    to_restart: bool,
    running_version: str,
    configured_version: str,
):
    """
    Changes the version or status of the service.
    """
    pass


@router.get(
    "/{service_id}/variables",
    response_model=Variables,
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
    response_model={},
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_service_schema(service_id: str):
    """
    Displays the service schema.
    """
    pass
