from fastapi import APIRouter

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.variables import Variables, VariableValidation

router = APIRouter()


@router.get(
    "/validate",
    response_model=VariableValidation,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_validate():
    pass
