import logging
from functools import wraps
from typing import Any, Callable, Coroutine, List, Optional, TypeVar

from sqlalchemy import and_, desc, func, or_, select, tuple_
from sqlalchemy.orm import Query, Session, joinedload
from starlette.concurrency import run_in_threadpool
from tdp.core.collections import Collections
from tdp.core.dag import Dag, IllegalNodeError
from tdp.core.models import DeploymentLog, ServiceComponentLog
from tdp.core.runner import (
    DeploymentPlan,
    EmptyDeploymentPlanError,
    GeneratedDeploymentPlanMissesOperationError,
    NothingToRestartError,
    NothingToResumeError,
    UnsupportedDeploymentTypeError,
)
from tdp.core.variables import ClusterVariables

from tdp_server.schemas import DeployRequest, Operation, OperationsRequest, ResumeRequest

from .utils import operation_schema_from_operation

logger = logging.getLogger("tdp_server")

T = TypeVar("T")


def async_wrapper(func: Callable[..., T]) -> Callable[..., Coroutine[Any, Any, T]]:
    @wraps(func)
    def async_method(*args, **kwargs):
        return run_in_threadpool(func, *args, **kwargs)

    return async_method


class AsyncDeploymentPlan:

    from_dag = async_wrapper(DeploymentPlan.from_dag)
    from_operations = async_wrapper(DeploymentPlan.from_operations)
    from_failed_deployment = async_wrapper(DeploymentPlan.from_failed_deployment)
    from_reconfigure = async_wrapper(DeploymentPlan.from_reconfigure)


class DeploymentPlanService:
    @staticmethod
    async def from_request(dag: Dag, request: DeployRequest) -> DeploymentPlan:
        deployment_arguments = {} if request is None else request.dict()
        try:
            deployment_plan = await AsyncDeploymentPlan.from_dag(
                dag, **deployment_arguments
            )
        except (EmptyDeploymentPlanError, IllegalNodeError) as e:
            raise ValueError(e) from e
        return deployment_plan

    @staticmethod
    async def from_operations_request(
        collections: Collections, request: OperationsRequest
    ) -> DeploymentPlan:
        operations = []
        for target in request.operations:
            try:
                operation = collections.operations[target]
            except KeyError as e:
                raise ValueError(
                    f"target '{target}' is not a possible operation"
                ) from e
            if operation.noop:
                raise ValueError(
                    f"'{target}' is tagged as noop and thus"
                    " cannot be executed in an operations request"
                )
            operations.append(operation)
        return await AsyncDeploymentPlan.from_operations(operations)

    @staticmethod
    async def from_reconfigure_request(
        db: Session, dag: Dag, cluster_variables: ClusterVariables
    ):
        latest_successes = db.execute(
            get_latest_success_service_component_version_query()
        ).all()
        try:
            return await AsyncDeploymentPlan.from_reconfigure(
                dag, cluster_variables, latest_successes
            )
        except NothingToRestartError as e:
            raise ValueError("Nothing to restart") from e

    @staticmethod
    async def from_resume_request(
        db: Session, dag: Dag, resume_request: ResumeRequest
    ) -> DeploymentPlan:
        deployment_log = (
            db.execute(get_deployment_log_query(resume_request.id))
            .unique()
            .scalar_one_or_none()
        )
        if deployment_log is None:
            if resume_request.id is None:
                raise ValueError("No deployments yet")
            else:
                raise ValueError(f"Deployment {resume_request.id} does not exist")
        try:
            return await AsyncDeploymentPlan.from_failed_deployment(dag, deployment_log)
        except (
            GeneratedDeploymentPlanMissesOperationError,
            NothingToResumeError,
            UnsupportedDeploymentTypeError,
        ) as e:
            logger.exception(e)
            raise ValueError(str(e)) from e

    @staticmethod
    async def get_plan_as_list(deployment_plan: DeploymentPlan) -> List[Operation]:
        return await run_in_threadpool(
            list, map(operation_schema_from_operation, deployment_plan.operations)
        )


def get_latest_success_service_component_version_query() -> Query:
    latest_success_for_each_service = select(
        func.max(ServiceComponentLog.deployment_id),
        ServiceComponentLog.service,
        ServiceComponentLog.component,
    ).group_by(ServiceComponentLog.service, ServiceComponentLog.component)
    # Request with or_ because querying with a tuple of 3 attributes using in_ operator
    # does not work when the value can be null (because NULL in_ NULL is translated to `NULL = NULL` which returns NULL)
    return (
        select(
            ServiceComponentLog.service,
            ServiceComponentLog.component,
            ServiceComponentLog.version,
        )
        .filter(
            or_(
                tuple_(
                    ServiceComponentLog.deployment_id,
                    ServiceComponentLog.service,
                    ServiceComponentLog.component,
                ).in_(latest_success_for_each_service),
                and_(
                    tuple_(
                        ServiceComponentLog.deployment_id,
                        ServiceComponentLog.service,
                    ).in_(
                        select(
                            latest_success_for_each_service.c[0],
                            latest_success_for_each_service.c[1],
                        )
                    ),
                    ServiceComponentLog.component.is_(None),
                ),
            )
        )
        .order_by(
            desc(ServiceComponentLog.deployment_id),
            ServiceComponentLog.service,
            ServiceComponentLog.component,
        )
    )


def get_deployment_log_query(deployment_id: Optional[int] = None) -> Query:
    query = (
        select(DeploymentLog)
        .options(
            joinedload(DeploymentLog.service_components),
            joinedload(DeploymentLog.operations),
        )
        .order_by(desc(DeploymentLog.id))
        .limit(1)
    )
    if deployment_id is not None:
        query = query.where(DeploymentLog.id == deployment_id)
    return query
