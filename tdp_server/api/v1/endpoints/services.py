from fastapi import APIRouter
from fastapi_pagination.cursor import CursorPage

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.services import Service, ServiceUpdateResponse

router = APIRouter()


@router.get(
    "",
    response_model=CursorPage[str],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_services():
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
    pass


@router.put(
    "/{service_id}",
    response_model=ServiceUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def put_service(service_id: str):
    pass


@router.patch(
    "/{service_id}",
    response_model=ServiceUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def patch_service(service_id: str):
    pass


@router.post(
    "{service_id}/variables",
    response_model=Service,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def provide_service_variables(service_id: str):
    pass


@router.post(
    "{service_id}/schema",
    response_model={},
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def provide_service_schema(service_id: str):
    pass
