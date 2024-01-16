from fastapi import FastAPI
from fastapi_pagination import add_pagination
from logging.config import dictConfig
from typing import List

from tdp_server.api.v1.api import api_router
from tdp_server.log_config import logger


app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
add_pagination(app)

logger.info("Server ready")

def get_all_get_endpoints() -> List[str]:
    """
    Returns a list of all GET method URLs in the application
    """
    endpoints = set()
    for route in app.routes:
        if "GET" in route.methods:
            endpoints.add((route.path, route.endpoint.__name__))

    return [{"path": path, "method": method} for path, method in endpoints]


@app.get("/", response_model=List)
async def read_get_endpoints():
    """
    Lists all other GET method URLs
    """
    return get_all_get_endpoints()
