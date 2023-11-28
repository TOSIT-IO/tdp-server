from fastapi import APIRouter

from typing import List

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.status import CurrentStatus, StaleComponent

router = APIRouter()


@router.get(
    "/",
    response_model=List[CurrentStatus],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_services():
    pass


@router.post(
    "/stales",
    response_model=List[StaleComponent],
    responses={**dependencies.COMMON_RESPONSES},
)
def post_stales():
    pass
