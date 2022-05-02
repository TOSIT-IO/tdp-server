from multiprocessing import Process
from os import PathLike
from threading import Lock

from tdp.core.dag import Dag
from tdp.core.runner.action_runner import ActionRunner
from tdp.core.runner.ansible_executor import AnsibleExecutor
from tdp.core.service_manager import ServiceManager
from tdp_server.db.session import SessionLocal
from tdp_server.models import UserDeploymentLog


class StillRunningException(Exception):
    pass


class RunnerService:
    def __init__(
        self,
        dag: Dag,
        playbooks_directory: PathLike,
        run_directory: PathLike,
        tdp_vars: PathLike,
    ):
        self.dag = dag
        self.playbooks_directory = playbooks_directory
        self.run_directory = run_directory
        self.tdp_vars = tdp_vars
        self.process = None
        self._lock = Lock()

    def run_nodes(self, user, *args, **kwargs):
        with self._lock:
            if self.process:
                if self.process.is_alive():
                    raise StillRunningException("run_nodes is still running")
            self.process = RunnerProcess(
                self.dag,
                self.playbooks_directory,
                self.run_directory,
                self.tdp_vars,
                user,
                *args,
                **kwargs,
            )
            self.process.start()

    @property
    def running(self) -> bool:
        return not self.process is None and self.process.is_alive()


class RunnerProcess(Process):
    def __init__(
        self,
        dag: Dag,
        playbooks_directory: PathLike,
        run_directory: PathLike,
        tdp_vars: PathLike,
        user: str,
        *args,
        **kwargs,
    ) -> None:
        super(RunnerProcess, self).__init__()
        self.dag = dag
        self.playbooks_directory = playbooks_directory
        self.run_directory = run_directory
        self.tdp_vars = tdp_vars
        self.user = user
        self.args = args
        self.kwargs = kwargs

    def run(self):
        executor = AnsibleExecutor(self.playbooks_directory, self.run_directory)
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
