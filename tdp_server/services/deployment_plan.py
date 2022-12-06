from functools import wraps
from typing import Any, Callable, Coroutine, List, TypeVar

from starlette.concurrency import run_in_threadpool
from tdp.core.collections import Collections
from tdp.core.dag import Dag, IllegalNodeError
from tdp.core.runner import DeploymentPlan, EmptyDeploymentPlanError

from tdp_server.schemas import DeployRequest, Operation, RunRequest

from .utils import operation_schema_from_operation

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
    async def from_run_request(
        collections: Collections, request: RunRequest
    ) -> DeploymentPlan:
        operations = []
        for target in request.targets:
            try:
                operation = collections.operations[target]
            except KeyError as e:
                raise ValueError(
                    f"target '{target}' is not a possible operation"
                ) from e
            if operation.noop:
                raise ValueError(
                    f"'{target}' is tagged as noop and thus"
                    " cannot be executed in a run request"
                )
            operations.append(operation)
        return await AsyncDeploymentPlan.from_operations(operations)

    @staticmethod
    async def get_plan_as_list(deployment_plan: DeploymentPlan) -> List[Operation]:
        return await run_in_threadpool(
            list, map(operation_schema_from_operation, deployment_plan.operations)
        )
