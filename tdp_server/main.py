import logging
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from tdp_server.api.v1.api import api_router
from tdp_server.core.config import settings
from tdp_server.core.log_config import init_loggers

init_loggers()

logger = logging.getLogger("tdp_server")
logger.setLevel(settings.LOG_LEVEL)


def create_app() -> FastAPI:

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
    app.include_router(api_router, prefix=settings.API_V1_STR)
    return app


app = create_app()


@app.middleware("http")
async def cache_control_middleware(request: Request, call_next: Callable):
    response: Response = await call_next(request)
    if request.method == "GET" and not "Cache-Control" in response.headers:
        response.headers["Cache-Control"] = "no-cache"
    return response


@app.get("/")
async def root():
    return {"message": settings.PROJECT_NAME}
