import logging
from typing import List

from fastapi import APIRouter, Depends
from tdp.core.collections import Collections
from tdp.core.dag import Dag

from tdp_server.api import dependencies
from tdp_server.services import Operations

logger = logging.getLogger("tdp_server")
router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=List[str],
    responses={**dependencies.COMMON_RESPONSES},
)
async def get_operations(
    *,
    collections: Collections = Depends(dependencies.get_collections),
) -> List[str]:
    """Returns every operations possible"""
    return await Operations.get_operations(collections)


@router.get(
    "/dag",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=List[str],
    responses={**dependencies.COMMON_RESPONSES},
)
async def get_dag_operations(
    *,
    dag: Dag = Depends(dependencies.get_dag),
) -> List[str]:
    """Return list of every dag operation, topologically sorted"""
    return await Operations.get_dag_operations(dag)


@router.get(
    "/other",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=List[str],
    responses={**dependencies.COMMON_RESPONSES},
)
async def get_other_operations(
    *,
    collections: Collections = Depends(dependencies.get_collections),
) -> List[str]:
    """Returns operations outside of the dag"""
    return await Operations.get_other_operations(collections)
