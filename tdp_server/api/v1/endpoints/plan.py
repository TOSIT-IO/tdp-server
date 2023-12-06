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
def post_plan_dag(options: PlanOptionsDag):
    pass


@router.post(
    "/operations",
    response_model=List[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def post_plan_operations(option: PlanOptionsOperations):
    pass


@router.post(
    "/resume",
    response_model=List[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def post_plan_resume(options: PlanOptionsCommon):
    pass


@router.post(
    "/reconfigure",
    response_model=List[Operation],
    responses={**dependencies.COMMON_RESPONSES},
)
def post_plan_reconfigure(Options: PlanOptionsReconfigure):
    pass


@router.post(
    "/import",
    response_model=List[Operation],
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.IMPORT_FILE_DOES_NOT_EXIST,
    },
)
def post_import(options: Path):
    pass


@router.post(
    "/custom",
    response_model=List[Operation],
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.IMPORT_FILE_DOES_NOT_EXIST,
    },
)
def post_costum(options: PlanOptionsCostum):
    pass
