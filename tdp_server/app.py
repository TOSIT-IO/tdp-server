from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from tdp.core.dag import Dag
from tdp.core.deployment import AnsibleExecutor, DeploymentRunner, Executor
from tdp.core.variables import ClusterVariables

from tdp_server.api.v1.api import api_router
from tdp_server.core.config import settings
from tdp_server.db.session import SessionLocal
from tdp_server.schemas.oauth2 import SCOPES
from tdp_server.services import RunnerService
from tdp_server.services.oauth2 import (
    AuthorizationServer,
    ResourceProtector,
    configure_authorization_server,
    configure_resource_protector,
)


def create_app(
    dag: Optional[Dag] = None,
    cluster_variables: Optional[ClusterVariables] = None,
    executor: Optional[Executor] = None,
    deployment_runner: Optional[DeploymentRunner] = None,
    runner_service: Optional[RunnerService] = None,
    authorization_server: Optional[AuthorizationServer] = None,
    resource_protector: Optional[ResourceProtector] = None,
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
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY, max_age=3600)

    app.include_router(api_router, prefix=settings.API_V1_STR)

    if dag is None:
        dag = Dag(settings.TDP_COLLECTIONS)

    if cluster_variables is None:
        cluster_variables = ClusterVariables.get_cluster_variables(settings.TDP_VARS)

    if executor is None:
        executor = AnsibleExecutor(settings.TDP_RUN_DIRECTORY, settings.MOCK_DEPLOY)

    if deployment_runner is None:
        deployment_runner = DeploymentRunner(
            settings.TDP_COLLECTIONS, executor, cluster_variables
        )

    if runner_service is None:
        runner_service = RunnerService(deployment_runner, settings.TDP_RUN_DIRECTORY)

    if authorization_server is None:
        authorization_server = AuthorizationServer(SessionLocal, list(SCOPES.keys()))
        configure_authorization_server(settings, authorization_server)

    if resource_protector is None:
        resource_protector = ResourceProtector()
        configure_resource_protector(SessionLocal, resource_protector)

    app.state.settings = settings
    app.state.dag = dag
    app.state.cluster_variables = cluster_variables
    app.state.executor = executor
    app.state.deployment_runner = deployment_runner
    app.state.runner_service = runner_service
    app.state.authorization = authorization_server
    app.state.protector = resource_protector

    return app
