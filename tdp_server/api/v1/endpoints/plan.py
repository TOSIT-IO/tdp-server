from fastapi import APIRouter
from typing import List, Optional
from pathlib import Path

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.plan import PlanOptionsDag, PlanDag
from tdp_server.schemas.operations import Operation
from tdp.core.models.operation_model import OperationModel

router = APIRouter()


@router.post(
    "/dag",
    response_model=List[PlanDag],
    responses={**dependencies.COMMON_RESPONSES},
)
def plan_dag(
    preview: bool = False,
    options: Optional[PlanOptionsDag] = None,
    filter: Optional[str] = None,
):
    """
    Plans from the DAG.

    options:

    - restart: bool

    - reverse: bool

    - stop: bool
    """
    pass


@router.post(
    "/operations",
    response_model=List[PlanDag],
    responses={**dependencies.COMMON_RESPONSES},
)
def plan_operations(operation_names: str, extra_vars: str, hosts: str):
    """
    Runs a list of operations.
    """
    pass


@router.post(
    "/resume",
    response_model=List[PlanDag],
    responses={**dependencies.COMMON_RESPONSES},
)
def plan_resume(preview: bool = False):
    """
    Resumes a failed or stopped deployment.
    """
    pass


@router.post(
    "/reconfigure",
    response_model=List[PlanDag],
    responses={**dependencies.COMMON_RESPONSES},
)
def plan_reconfigure(preview: bool = None, rolling_interval: Optional[int] = None):
    """
    Renconfigures required TDP services.
    """
    pass


@router.post(
    "/import",
    response_model=List[PlanDag],
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
    response_model=List[PlanDag],
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.IMPORT_FILE_DOES_NOT_EXIST,
    },
)
def plan_costum(
    operations: List[str],
    extra_vars: str,
    hosts: str,
    options: Optional[PlanOptionsDag] = None,
):
    """
    Customizes an existing plan.

    options:

    - restart: bool

    - reverse: bool

    - stop: bool
    """
    pass
