from fastapi import APIRouter
from fastapi_pagination import Page

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.operations import Operation

router = APIRouter()


@router.post(
    "/dag",
    response_model=Page[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def post_plan_dag():
    pass


@router.post(
    "/operations",
    response_model=Page[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def post_plan_operations():
    pass


@router.post(
    "/resume",
    response_model=Page[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def post_plan_resume():
    pass


@router.post(
    "/reconfigure",
    response_model=Page[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def post_plan_reconfigure():
    pass


@router.post(
    "/import",
    response_model=Page[Operation],
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.IMPORT_FILE_DOES_NOT_EXIST,
    },
)
def post_import():
    pass
