import logging
from functools import partial
from pathlib import Path

from fastapi import BackgroundTasks
from filelock import FileLock, Timeout
from sqlalchemy.orm.session import Session, sessionmaker
from starlette.concurrency import run_in_threadpool
from tdp.core.dag import Dag
from tdp.core.runner import (
    DeploymentIterator,
    DeploymentPlan,
    DeploymentRunner,
    EmptyDeploymentPlanError,
)

from tdp_server.models import UserDeploymentLog
from tdp_server.schemas import DeploymentLog, DeployRequest

from .utils import deployment_from_deployment_log

logger = logging.getLogger("tdp_server")


class StillRunningException(Exception):
    pass


class RunnerService:
    def __init__(
        self,
        deployment_runner: DeploymentRunner,
        lock_dir: Path,
    ):
        self.deployment_runner = deployment_runner
        # Timeout 0 makes it non blocking on every `acquire` call
        self._file_lock = partial(FileLock, lock_dir / ".deploy.lock", timeout=0)

    async def run(
        self,
        background_tasks: BackgroundTasks,
        session_local: sessionmaker,
        user: str,
        deployment_plan: DeploymentPlan,
    ) -> DeploymentLog:
        lock = self._file_lock()
        try:
            lock.acquire()
            with session_local() as session:
                deployment_iterator = (
                    await self._get_deployment_iterator_and_insert_in_db(
                        session, user, deployment_plan
                    )
                )
                deployment = deployment_from_deployment_log(
                    deployment_iterator.log, user
                )
            background_tasks.add_task(
                self._background_iterate_operations,
                session_local,
                lock,
                deployment_iterator,
            )
            return deployment
        except Timeout as e:
            raise StillRunningException("Failed to lock process for deployment") from e
        except Exception as e:
            if lock.is_locked:
                lock.release()
            raise e

    async def _get_deployment_iterator_and_insert_in_db(
        self, session: Session, user: str, deployment_plan: DeploymentPlan
    ) -> DeploymentIterator:
        deployment_iterator = await run_in_threadpool(
            self.deployment_runner.run, deployment_plan
        )
        user_deployment_log = UserDeploymentLog(
            user_identifier=user,
            deployment=deployment_iterator.log,
        )
        session.add(user_deployment_log)
        # insert pending deployment log
        session.commit()
        return deployment_iterator

    def _background_iterate_operations(
        self,
        session_local: sessionmaker,
        lock: FileLock,
        deployment_iterator: DeploymentIterator,
    ):
        try:
            with session_local() as session:
                for operation_log, service_component_log in deployment_iterator:
                    session.add(operation_log)
                    if service_component_log is not None:
                        session.add(service_component_log)
                    session.commit()
                # notify sqlalchemy deployment log has been updated
                session.merge(deployment_iterator.log)
                session.commit()
        except Exception as e:
            logger.exception(e)
        finally:
            lock.release()

    @property
    def running(self) -> bool:
        try:
            lock = self._file_lock()
            with lock.acquire():
                return False
        except Timeout:
            return True
