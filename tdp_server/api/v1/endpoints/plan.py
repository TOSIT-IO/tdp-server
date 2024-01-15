# from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_pagination.cursor import CursorPage
from typing import List, Optional
from pathlib import Path

from tdp.cli.commands.plan.dag import dag
from tdp.core.collections import Collections
from tdp_server.api.v1 import dependencies
from tdp_server.core.config import settings, collections
from tdp_server.schemas.plan import PlanDag, PlanOperations


from typing import Optional

from tdp.cli.queries import get_planned_deployment
from tdp.cli.session import get_session

from tdp.core.dag import Dag
from tdp.core.models import DeploymentModel, FilterTypeEnum


router = APIRouter()

logger = logging.getLogger("tdp_server_logger.plan")

database_dsn = settings.TDP_DATABASE_DSN


@router.get(
    "",
    response_model=CursorPage[PlanDag],
    responses={**dependencies.COMMON_RESPONSES},
)
def show_plan():
    """
    Shows the latest plan.
    """
    with get_session(database_dsn, commit_on_exit=True) as session:
        planned_deployment = get_planned_deployment(session)
        if planned_deployment:
            operation_list = [o.to_dict() for o in planned_deployment.operations]
            output = {
                "deployment_id": planned_deployment.id,
                "state": planned_deployment.state,
                "deployment_type": planned_deployment.deployment_type,
                "operations": operation_list,
                "options": planned_deployment.options,
            }
            logger.info("GET show_plan Success")
            return JSONResponse(content=output)
        else:
            message = "No planned deployment"
            logger.error(message)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=message,
            )


@router.post(
    "/dag",
    response_model=PlanDag,
    responses={**dependencies.COMMON_RESPONSES},
)
async def plan_dag(
    targets: str = None,
    sources: str = None,
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

    def dag(
        sources: tuple[str],
        targets: tuple[str],
        restart: bool,
        preview: bool,
        collections: Collections,
        database_dsn: str,
        reverse: bool,
        stop: bool,
        filter: Optional[str] = None,
        rolling_interval: Optional[int] = None,
    ):
        """Deploy from the DAG."""
        if stop and restart:
            logger.error("Cannot use `--restart` and `--stop` at the same time.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Cannot use `--restart` and `--stop` at the same time.",
            )
        dag = Dag(collections)
        set_nodes = set()
        if sources:
            set_nodes.update(sources)
        if targets:
            set_nodes.update(targets)
        set_difference = set_nodes.difference(dag.operations)
        if set_difference:
            logger.error(f"{set_difference} are not valid nodes.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{set_difference} are not valid nodes.",
            )

        if sources:
            logger.info(f"Creating a deployment plan from: {sources}")
        elif targets:
            logger.info(f"Creating a deployment plan to: {targets}")
        else:
            logger.info("Creating a deployment plan for the whole DAG.")

        try:
            deployment = DeploymentModel.from_dag(
                dag,
                sources=sources,
                targets=targets,
                filter_expression=filter,
                filter_type=None,
                restart=restart,
                reverse=reverse,
                stop=stop,
                rolling_interval=rolling_interval,
            )
            operation_list = [o.to_dict() for o in deployment.operations]
            output = {
                "deployment_id": deployment.id,
                "state": deployment.state,
                "deployment_type": deployment.deployment_type,
                "operations": operation_list,
                "options": deployment.options,
            }
            if preview:
                logger.info("DAG preview successfully planned")
                return output

            with get_session(database_dsn, commit_on_exit=True) as session:
                planned_deployment = get_planned_deployment(session)
                if planned_deployment:
                    deployment.id = planned_deployment.id
                session.merge(deployment)
                [
                    o.update({"deployment_id": get_planned_deployment(session).id})
                    for o in operation_list
                ]
                output.update({"deployment_id": get_planned_deployment(session).id})
                logger.info("DAG successfully planned")
                return output
        except Exception as error:
            logger.error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={f"{type(error).__name__}": f"{error}"},
            )

    message = dag(
        sources,
        targets,
        restart,
        preview,
        collections,
        database_dsn,
        reverse,
        stop,
        filter,
        rolling_interval,
    )
    return JSONResponse(content=message)


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
