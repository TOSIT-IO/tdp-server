from fastapi import FastAPI
from tdp_server.api.v1.api import api_router


app = FastAPI()
app.include_router(api_router)


@app.get("/")
async def root():
    return {"tdp-server"}
