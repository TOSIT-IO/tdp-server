from fastapi import FastAPI, APIRouter
from fastapi_pagination import add_pagination
from typing import List

from tdp_server.api.v1.api import api_router


app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
add_pagination(app)


@app.get("/")
async def root():
    return {"tdp-server"}


def get_all_get_endpoints() -> List[str]:
    """
    Returns a list of all GET method URLs in the application
    """
    get_endpoints = []
    [get_endpoints.append(route.path) for route in app.routes if "GET" in route.methods]
    return get_endpoints[4:]


@app.get("/get-endpoints", response_model=List[str])
async def read_get_endpoints():
    """
    Lists all other GET method URLs
    """
    return get_all_get_endpoints()
