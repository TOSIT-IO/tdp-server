from fastapi import APIRouter

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.operations import Operation


router = APIRouter()


@router.get(
    "/",
    response_model=Operation,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_operations():
    pass


@router.get(
    "/dag",
    response_model=Operation,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_dag_operations():
    pass


@router.get(
    "/other",
    response_model=Operation,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_other_operations():
    pass
