from fastapi import APIRouter
from typing import List

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.operations import Operation

router = APIRouter()


@router.post(
    "/dag",
    response_model=List[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def post_plan_dag():
    pass


@router.post(
    "/operations",
    response_model=List[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def post_plan_operations():
    pass


@router.post(
    "/resumption",
    response_model=List[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def post_plan_resumption():
    pass


@router.post(
    "/reconfiguration",
    response_model=List[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def post_plan_reconfiguration():
    pass


@router.post(
    "/importation",
    response_model=List[Operation],
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.IMPORT_FILE_DOES_NOT_EXIST,
    },
)
def post_importation():
    pass
