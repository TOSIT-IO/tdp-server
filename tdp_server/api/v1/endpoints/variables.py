from fastapi import APIRouter
from fastapi_pagination import Page

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.variables import Variables, VariableValidation

router = APIRouter()


@router.get(
    "/",
    response_model=Page[Variables],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_variables():
    pass


@router.get(
    "/validate",
    response_model=VariableValidation,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_validate():
    pass


@router.get(
    "/schemas",
    response_model=dict,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_schemas():
    pass
