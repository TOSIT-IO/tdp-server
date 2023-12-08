from fastapi import APIRouter
from typing import List
from pathlib import Path

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.plan import (
    PlanOptionsCommon,
    PlanOptionsDag,
    PlanOptionsOperations,
    PlanOptionsReconfigure,
    PlanOptionsCostum,
)
from tdp_server.schemas.operations import Operation

router = APIRouter()


@router.post(
    "/dag",
    response_model=List[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def plan_dag(options: PlanOptionsDag):
    """
    Plans from the DAG.
    """
    pass


@router.post(
    "/operations",
    response_model=List[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def plan_operations(option: PlanOptionsOperations):
    """
    Runs a list of operations.
    """
    pass


@router.post(
    "/resume",
    response_model=List[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def plan_resume(options: PlanOptionsCommon):
    """
    Resumes a failed or stopped deployment.
    """
    pass


@router.post(
    "/reconfigure",
    response_model=List[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def plan_reconfigure(Options: PlanOptionsReconfigure):
    """
    Renconfigures required TDP services.
    """
    pass


@router.post(
    "/import",
    response_model=List[Operation],
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
    response_model=List[Operation],
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.IMPORT_FILE_DOES_NOT_EXIST,
    },
)
def plan_costum(options: PlanOptionsCostum):
    """
    Customizes an existing plan.
    """
    pass
