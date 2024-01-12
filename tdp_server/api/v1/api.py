from fastapi import APIRouter
from tdp_server.api.v1.endpoints import (
    components,
    configurations,
    services,
    deployments,
    deploy,
    operations,
    plan,
    validate,
)


api_router = APIRouter()

api_router.include_router(
    configurations.router, prefix="/configurations", tags=["configurations"]
)
api_router.include_router(
    validate.router, prefix="/configurations", tags=["configurations"]
)
api_router.include_router(
    services.router, prefix="/configurations/services", tags=["configurations"]
)
api_router.include_router(
    components.router,
    prefix="/configurations/services/{service_id}/components",
    tags=["configurations"],
)
api_router.include_router(
    deployments.router, prefix="/deployments", tags=["deployments"]
)
api_router.include_router(deploy.router, prefix="/deploy", tags=["deploy"])
api_router.include_router(operations.router, prefix="/operations", tags=["operations"])
api_router.include_router(plan.router, prefix="/plan", tags=["plan"])
