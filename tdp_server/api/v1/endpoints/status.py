from fastapi import APIRouter
from fastapi_pagination.cursor import CursorPage

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.status import CurrentStatus

router = APIRouter()


@router.get(
    "",
    response_model=CursorPage[CurrentStatus],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_status():
    """
    Shows service and component status.
    """
    pass
