from fastapi import APIRouter

from typing import List
from tdp_server.api.v1 import dependencies
from tdp_server.schemas.components import (
    Component,
    ComponentUpdateResponse,
    CurrentStatus,
    StaleComponent,
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
def get_component():
    pass


@router.put(
    "/{component_id}",
    response_model=ComponentUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def put_component():
    pass


@router.patch(
    "/{component_id}",
    response_model=ComponentUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def patch_component():
    pass


@router.post(
    "/{component_id}/variables",
    response_model=Component,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def post_component_variables():
    pass


@router.get(
    "/status",
    response_model=List[CurrentStatus],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_services():
    pass


@router.post(
    "/stales",
    response_model=List[StaleComponent],
    responses={**dependencies.COMMON_RESPONSES},
)
def post_stales():
    pass
