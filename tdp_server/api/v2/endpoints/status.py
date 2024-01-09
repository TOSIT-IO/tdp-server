from fastapi import APIRouter
from fastapi_pagination.cursor import CursorPage
from typing import Optional

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.configurations import CurrentStatus, StatusHistory
from tdp_server.schemas.components import (
    Component,
    Components,
    ComponentUpdateResponse,
)
from tdp_server.schemas.services import (
    Service,
    ServiceConf,
    ServiceUpdateResponse,
)


router = APIRouter()


@router.get(
    "",
    response_model=CursorPage[CurrentStatus],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_status():
    """
    Shows service and component status.
    """
    raise NotImplementedError


@router.get(
    "/history",
    response_model=CursorPage[StatusHistory],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_history():
    """
    Shows service and component status history.
    """
    raise NotImplementedError


@router.get(
    "",
    response_model=CursorPage[Service],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_services():
    """
    Returns a list of services.
    """
    raise NotImplementedError


@router.get(
    "/{service_id}",
    response_model=ServiceConf,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_service(service_id: str):
    """
    Returns the chosen service details.
    """
    raise NotImplementedError


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
    to_config: Optional[bool] = None,
    to_restart: Optional[bool] = None,
    running_version: Optional[str] = None,
    configured_version: Optional[str] = None,
):
    """
    Changes the version or status of the service.
    """
    raise NotImplementedError


@router.get(
    "/{service_id}/history",
    response_model=CursorPage[StatusHistory],
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_service_history(service_id):
    """
    Show history of a service's running and configured versions.
    """
    raise NotImplementedError


@router.get(
    "/{service_id}/components",
    response_model=Components,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_components(service_id: str):
    """
    Returns a list of components of a service.
    """
    raise NotImplementedError


@router.get(
    "/{service_id}/components/{component_id}",
    response_model=Component,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_component(service_id: str, component_id: str):
    """
    Returns the chosen component details.
    """
    raise NotImplementedError


@router.put(
    "/{service_id}/components/{component_id}",
    response_model=ComponentUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def put_component(
    service_id: str,
    component_id: str,
    to_config: Optional[bool] = None,
    to_restart: Optional[bool] = None,
    running_version: Optional[str] = None,
    configured_version: Optional[str] = None,
):
    """
    Changes the version or status of the component.
    """
    raise NotImplementedError


@router.get(
    "/{service_id}/components/{component_id}/history",
    response_model=CursorPage[StatusHistory],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_component_history(service_id: str, component_id: str, host: str):
    """
    Show history of a component's running and configured versions.
    """
    raise NotImplementedError
