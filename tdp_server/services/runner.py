from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from os import PathLike

from fasteners import InterProcessLock
from tdp.core.dag import Dag
from tdp.core.runner.action_runner import ActionRunner
from tdp.core.runner.ansible_executor import AnsibleExecutor
from tdp.core.service_manager import ServiceManager

from tdp_server.core.config import settings
from tdp_server.db.session import SessionLocal
from tdp_server.models import UserDeploymentLog

DEPLOY_LOCK = InterProcessLock(settings.TDP_RUN_DIRECTORY / ".deploy.lock")
RUN_LOCK = InterProcessLock(settings.TDP_RUN_DIRECTORY / ".run.lock")


class StillRunningException(Exception):
    pass


class RunnerService:
    def __init__(
        self,
        dag: Dag,
        run_directory: PathLike,
        tdp_vars: PathLike,
    ):
        self.dag = dag
        self.run_directory = run_directory
        self.tdp_vars = tdp_vars
        self.process = None

    def run_nodes(self, user, *args, **kwargs):
        is_locked = DEPLOY_LOCK.acquire(blocking=False)
        if not is_locked:
            raise StillRunningException("Failed to lock for deployment")
        try:
            if self.process:
                if self.process.is_alive():
                    raise StillRunningException("run_nodes is still running")
            parent_conn, child_conn = Pipe()
            self.process = RunnerProcess(
                self.dag,
                self.run_directory,
                self.tdp_vars,
                user,
                child_conn,
                *args,
                **kwargs,
            )
            self.process.start()
            result = parent_conn.recv()
            parent_conn.close()
            if result != 0:
                raise StillRunningException(
                    "RunnerProcess failed to lock for execution"
                )
        finally:
            DEPLOY_LOCK.release()

    @property
    def running(self) -> bool:
        return not self.process is None and self.process.is_alive()


class RunnerProcess(Process):
    def __init__(
        self,
        dag: Dag,
        run_directory: PathLike,
        tdp_vars: PathLike,
        user: str,
        child_conn: Connection,
        *args,
        **kwargs,
    ) -> None:
        super(RunnerProcess, self).__init__()
        self.dag = dag
        self.run_directory = run_directory
        self.tdp_vars = tdp_vars
        self.user = user
        self.child_conn = child_conn
        self.args = args
        self.kwargs = kwargs

    def send_status_to_parent(self, is_locked):
        status = 0 if is_locked else 1
        self.child_conn.send(status)
        self.child_conn.close()

    def run(self):
        is_locked = RUN_LOCK.acquire(blocking=False)
        try:
            self.send_status_to_parent(is_locked)
            if not is_locked:
                return
            executor = AnsibleExecutor(self.run_directory)
            runner = ActionRunner(
                self.dag,
                executor,
                ServiceManager.get_service_managers(self.dag, self.tdp_vars),
            )
            result = runner.run_nodes(*self.args, **self.kwargs)
            user_deployment_log = UserDeploymentLog(
                user=self.user,
            )
            user_deployment_log.deployment = result
            with SessionLocal() as db:
                db.add(user_deployment_log)
                db.commit()
        finally:
            RUN_LOCK.release()
