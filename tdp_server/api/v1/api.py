from fastapi import APIRouter
from tdp_server.api.v1.endpoints import (
    components,
    services,
    deployments,
    operations,
    planification,
    status,
    variables,
)


api_router = APIRouter()

api_router.include_router(services.router, prefix="/services", tags=["services"])
api_router.include_router(
    components.router, prefix="/services/{service_id}/components", tags=["components"]
)
api_router.include_router(
    deployments.router, prefix="/deployments", tags=["deployments"]
)
api_router.include_router(variables.router, prefix="/variables", tags=["variables"])
api_router.include_router(operations.router, prefix="/operations", tags=["operations"])
api_router.include_router(status.router, prefix="/status", tags=["status"])
api_router.include_router(
    planification.router, prefix="/planification", tags=["planification"]
)
