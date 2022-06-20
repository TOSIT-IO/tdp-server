from fastapi import APIRouter

from tdp_server.api.v1.endpoints import component, deploy, service

api_router = APIRouter()

api_router.include_router(service.router, prefix="/service", tags=["services"])
api_router.include_router(component.router, prefix="/service", tags=["components"])
api_router.include_router(deploy.router, prefix="/deploy", tags=["deploy"])
