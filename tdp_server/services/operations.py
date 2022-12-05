from typing import List

from pydantic import parse_obj_as
from starlette.concurrency import run_in_threadpool
from tdp.core.collections import Collections
from tdp.core.dag import Dag
from tdp.core.operation import Operation as tdp_Operation

from tdp_server.schemas import Operation

from .utils import operation_schema_from_operation


class Operations:
    @staticmethod
    async def get_operations(collections: Collections) -> List[Operation]:
        operation_to_schema = map(
            operation_schema_from_operation, collections.operations.values()
        )
        return await run_in_threadpool(list, operation_to_schema)

    @staticmethod
    async def get_dag_operations(dag: Dag) -> List[Operation]:
        operations = await run_in_threadpool(dag.get_all_operations)
        operation_to_schema = map(operation_schema_from_operation, operations)
        return await run_in_threadpool(list, operation_to_schema)

    @staticmethod
    async def get_other_operations(collections: Collections) -> List[Operation]:
        operation_to_schema = map(
            operation_schema_from_operation, collections.other_operations.values()  # type: ignore other_operations is never None
        )
        return await run_in_threadpool(list, operation_to_schema)
