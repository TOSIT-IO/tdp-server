from fastapi import APIRouter
from fastapi_pagination.cursor import CursorPage
from typing import Optional

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.operations import Operation, Operationtype


router = APIRouter()


@router.get(
    "/{Operationtype}",
    response_model=CursorPage[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_operations(options: Optional[Operationtype] = None):
    """
    Returns a list of operations.

    Options:

    - Dag: shows operations from DAG.

    - Other: shows other operations.
    """
    pass
