from fastapi import APIRouter
from fastapi_pagination.cursor import CursorPage
from typing import List, Optional
from pathlib import Path

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.plan import PlanDag, PlanOperations


router = APIRouter()


@router.get(
    "",
    response_model=CursorPage[PlanDag],
    responses={**dependencies.COMMON_RESPONSES},
)
def show_plan():
    """
    Shows the latest plan.
    """
    pass


@router.post(
    "/dag",
    response_model=PlanDag,
    responses={**dependencies.COMMON_RESPONSES},
)
def plan_dag(
    targets: str,
    source: str,
    restart: bool = False,
    reverse: bool = False,
    stop: bool = False,
    preview: bool = False,
    filter: Optional[str] = None,
    rolling_interval: Optional[int] = None,
):
    """
    Plans from the DAG.
    """
    pass


@router.post(
    "/operations",
    response_model=List[PlanOperations],
    responses={**dependencies.COMMON_RESPONSES},
)
def plan_operations(
    operation_names: str,
    extra_vars: str,
    hosts: str,
    preview: bool = False,
    rolling_interval: Optional[int] = None,
):
    """
    Runs a list of operations.
    """
    pass


@router.post(
    "/resume",
    response_model=PlanDag,
    responses={**dependencies.COMMON_RESPONSES},
)
def plan_resume(id: int, preview: bool = False):
    """
    Resumes a failed or stopped deployment.
    """
    pass


@router.post(
    "/reconfigure",
    response_model=PlanDag,
    responses={**dependencies.COMMON_RESPONSES},
)
def plan_reconfigure(preview: bool = None, rolling_interval: Optional[int] = None):
    """
    Renconfigures required TDP services.
    """
    pass


@router.post(
    "/import",
    response_model=PlanDag,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.IMPORT_FILE_DOES_NOT_EXIST,
    },
)
def plan_from_import(options: Path):
    """
    Plans from an imported file.
    """
    pass


@router.post(
    "/custom",
    response_model=PlanDag,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.IMPORT_FILE_DOES_NOT_EXIST,
    },
)
def plan_custom(
    operations: List[str],
    extra_vars: str,
    hosts: str,
    restart: bool = False,
    reverse: bool = False,
    stop: bool = False,
):
    """
    Customizes an existing plan.

    options:

    - restart: bool

    - reverse: bool

    - stop: bool
    """
    pass
