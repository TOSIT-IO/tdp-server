from fastapi import FastAPI
from fastapi_pagination import add_pagination
from tdp_server.api.v1.api import api_router


app = FastAPI()
app.include_router(api_router)
add_pagination(app)


@app.get("/")
async def root():
    return {"tdp-server"}
