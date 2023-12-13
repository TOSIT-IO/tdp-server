from fastapi import APIRouter
from fastapi_pagination.cursor import CursorPage
from typing import List

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.common import StateEnum
from tdp_server.schemas.components import (
    Component,
    ComponentUpdateResponse,
    ComponentGenerateStalesOptions,
    StaleComponent,
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
    service_id: str, component_id: str, options: Component, status: StateEnum
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
    response_model=StatusHistory,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_component_history(service_id: str, component_id: str):
    """
    Show history of all services and components running and configured versions.
    """
    pass


@router.post(
    "/{component_id}/stales",
    response_model=List[StaleComponent],
    responses={**dependencies.COMMON_RESPONSES},
)
def provide_stales(
    service_id: str, component_id: str, options: ComponentGenerateStalesOptions
):
    """
    Pass the component to stale.
    """
    pass
