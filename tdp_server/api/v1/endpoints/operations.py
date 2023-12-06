from fastapi import APIRouter
from typing import Optional

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.operations import Operation, Operationtype


router = APIRouter()


@router.get(
    "",
    response_model=Operation,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_operations(options: Optional[Operationtype] = None):
    pass
