import logging
from functools import partial
from pathlib import Path

from fastapi import BackgroundTasks
from filelock import FileLock, Timeout
from sqlalchemy.orm.session import sessionmaker
from tdp.core.runner.operation_runner import OperationRunner

from tdp_server.models import UserDeploymentLog

logger = logging.getLogger("tdp_server")


class StillRunningException(Exception):
    pass


class RunnerService:
    def __init__(
        self,
        operation_runner: OperationRunner,
        lock_dir: Path,
    ):
        self.operation_runner = operation_runner
        # Timeout 0 makes it non blocking on every `acquire` call
        self._file_lock = partial(FileLock, lock_dir / ".deploy.lock", timeout=0)

    def run_nodes(
        self,
        background_tasks: BackgroundTasks,
        session_local: sessionmaker,
        user: str,
        *args,
        **kwargs,
    ):
        lock = self._file_lock()
        try:
            lock.acquire()
            background_tasks.add_task(
                partial(self._background_run_node, session_local, lock, user),
                *args,
                **kwargs,
            )
        except Timeout as e:
            raise StillRunningException("Failed to lock process for deployment") from e
        except Exception as e:
            if lock.is_locked:
                lock.release()
            raise e

    def _background_run_node(
        self, session_local: sessionmaker, lock: FileLock, user: str, *args, **kwargs
    ):
        try:
            with session_local() as session:
                operation_iterator = self.operation_runner.run_nodes(*args, **kwargs)
                user_deployment_log = UserDeploymentLog(
                    user_identifier=user,
                    deployment=operation_iterator.deployment_log,
                )
                session.add(user_deployment_log)
                # insert pending deployment log
                session.commit()
                for operation in operation_iterator:
                    session.add(operation)
                    session.commit()
                # notify sqlalchemy deployment log has been updated
                session.merge(operation_iterator.deployment_log)
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
