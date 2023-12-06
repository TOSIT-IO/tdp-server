from fastapi import APIRouter
from fastapi_pagination.cursor import CursorPage
from typing import List

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.components import (
    Component,
    ComponentUpdateResponse,
    ComponentGenerateStalesOptions,
    StaleComponent,
    StatusHistory,
)

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
    pass


@router.post(
    "/{component_id}/variables",
    response_model=ComponentUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def provide_component_variables(
    service_id: str, component_id: str, component: Component
):
    pass


@router.get(
    "/{component_id}/status-history",
    response_model=StatusHistory,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_component_history(service_id: str, component_id: str):
    pass


@router.post(
    "/{component_id}/stales",
    response_model=List[StaleComponent],
    responses={**dependencies.COMMON_RESPONSES},
)
def provide_stales(
    service_id: str, component_id: str, options: ComponentGenerateStalesOptions
):
    pass
