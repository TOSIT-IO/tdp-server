import logging
from typing import Callable

from fastapi import Request, Response

from tdp_server.app import create_app
from tdp_server.core.config import settings
from tdp_server.core.log_config import init_loggers

init_loggers()

logger = logging.getLogger("tdp_server")
logger.setLevel(settings.LOG_LEVEL)

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
