from fastapi import APIRouter

from tdp_server.api.v1.endpoints import (
    component,
    deploy,
    operation,
    plan,
    schema,
    service,
)

api_router = APIRouter()

api_router.include_router(service.router, prefix="/service", tags=["services"])
api_router.include_router(
    component.router, prefix="/service/{service_id}/component", tags=["components"]
)
api_router.include_router(deploy.router, prefix="/deploy", tags=["deploy"])
api_router.include_router(operation.router, prefix="/operation", tags=["operation"])
api_router.include_router(plan.router, prefix="/plan", tags=["plan"])
api_router.include_router(schema.router, prefix="/schema", tags=["schema"])
