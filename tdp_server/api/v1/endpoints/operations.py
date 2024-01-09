from fastapi import APIRouter
from fastapi_pagination.cursor import CursorPage
from typing import Optional

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.operations import Operation, Operationtype


router = APIRouter()


@router.get(
    "",
    response_model=CursorPage[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_operations(
    hosts: str, topo_sort: bool = False, options: Optional[Operationtype] = None
):
    """
    Returns a list of operations.

    Options:

    - DAG: shows operations from DAG.

    - OTHER: shows other operations.

    - Displays DAG operations in topological order, only works if options = DAG
    """
    raise NotImplementedError
