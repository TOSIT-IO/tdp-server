from fastapi import APIRouter

from typing import List

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.variables import Variables, VariableValidation

router = APIRouter()


@router.get(
    "/",
    response_model=List[Variables],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_variables():
    pass


@router.get(
    "/validate",
    response_model=VariableValidation,
    responses={**dependencies.COMMON_RESPONSES},
)
def post_validate():
    pass
