from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from tdp.core.dag import Dag
from tdp.core.deployment import AnsibleExecutor, DeploymentRunner, Executor
from tdp.core.variables import ClusterVariables

from tdp_server.api.v1.api import api_router
from tdp_server.core.config import settings
from tdp_server.services.runner import RunnerService


def create_app(
    dag: Optional[Dag] = None,
    cluster_variables: Optional[ClusterVariables] = None,
    executor: Optional[Executor] = None,
    deployment_runner: Optional[DeploymentRunner] = None,
    runner_service: Optional[RunnerService] = None,
) -> FastAPI:

    app = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware)

    app.include_router(api_router, prefix=settings.API_V1_STR)

    if dag is None:
        dag = Dag(settings.TDP_COLLECTIONS)

    if cluster_variables is None:
        cluster_variables = ClusterVariables.get_cluster_variables(
            settings.TDP_COLLECTIONS, settings.TDP_VARS
        )

    if executor is None:
        executor = AnsibleExecutor(settings.TDP_RUN_DIRECTORY, settings.MOCK_DEPLOY)

    if deployment_runner is None:
        deployment_runner = DeploymentRunner(
            settings.TDP_COLLECTIONS, executor, cluster_variables
        )

    if runner_service is None:
        runner_service = RunnerService(deployment_runner, settings.TDP_RUN_DIRECTORY)

    app.state.settings = settings
    app.state.dag = dag
    app.state.cluster_variables = cluster_variables
    app.state.executor = executor
    app.state.deployment_runner = deployment_runner
    app.state.runner_service = runner_service

    return app
