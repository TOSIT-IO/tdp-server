from fastapi import APIRouter

from tdp_server.api.v1.endpoints import service

api_router = APIRouter()

api_router.include_router(service.router, prefix="/service", tags=["services"])
