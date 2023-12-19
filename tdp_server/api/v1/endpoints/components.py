from fastapi import APIRouter
from fastapi_pagination.cursor import CursorPage
from typing import List

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.components import (
    Component,
    ComponentUpdateResponse,
    StatusHistory,
)
from tdp_server.schemas.variables import Variables

router = APIRouter()


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
    pass


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
    to_config: bool,
    to_restart: bool,
    running_version: str,
    configured_version: str,
):
    """
    Changes the version or status of the component.
    """
    pass


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
    pass


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
    pass


@router.get(
    "/{component_id}/status-history",
    response_model=CursorPage[StatusHistory],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_component_history(service_id: str, component_id: str, host: str):
    """
    Show history of all services and components running and configured versions.
    """
    pass
