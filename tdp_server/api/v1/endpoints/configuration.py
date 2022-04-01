from fastapi import APIRouter
from fastapi_pagination.cursor import CursorPage

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.configuration import CurrentStatus, StatusHistory


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


@router.get(
    "/history",
    response_model=CursorPage[StatusHistory],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_history():
    """
    Shows service and component status history.
    """
    pass
