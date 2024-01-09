from fastapi import APIRouter
from fastapi_pagination.cursor import CursorPage
from typing import Optional

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.configurations import StatusHistory
from tdp_server.schemas.components import (
    Component,
    Components,
    ComponentUpdateResponse,
)
from tdp_server.schemas.variables import Variables

router = APIRouter()


@router.get(
    "",
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
    "/{component_id}",
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
    "/{component_id}",
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
    "/{component_id}/variables",
    response_model=Variables,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_component_variables(service_id: str, component_id: str):
    """
    Displays the component variables.
    """
    raise NotImplementedError


@router.put(
    "/{component_id}/variables",
    response_model=ComponentUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def provide_component_variables(
    service_id: str, component_id: str, component: Variables
):
    """
    Modifies the component variables.
    """
    raise NotImplementedError


@router.patch(
    "/{component_id}/variables",
    response_model=ComponentUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def patch_component_variables(service_id: str, component_id: str, component: Variables):
    """
    Patches the component variables.
    """
    raise NotImplementedError


@router.get(
    "/{component_id}/history",
    response_model=CursorPage[StatusHistory],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_component_history(service_id: str, component_id: str, host: str):
    """
    Show history of a component's running and configured versions.
    """
    raise NotImplementedError
