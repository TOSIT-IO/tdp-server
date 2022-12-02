from typing import List

from starlette.concurrency import run_in_threadpool
from tdp.core.collections import Collections
from tdp.core.dag import Dag


class Operations:
    @staticmethod
    async def get_operations(collections: Collections) -> List[str]:
        return await run_in_threadpool(list, collections.operations)

    @staticmethod
    async def get_dag_operations(dag: Dag) -> List[str]:
        operations = await run_in_threadpool(dag.get_all_operations)
        return await run_in_threadpool(list, map(lambda op: op.name, operations))

    @staticmethod
    async def get_other_operations(collections: Collections) -> List[str]:
        return await run_in_threadpool(list, collections.other_operations)
