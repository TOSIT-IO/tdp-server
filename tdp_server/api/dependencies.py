from functools import lru_cache
from typing import Dict, Generator

from fastapi import Depends, Security
from tdp.core.dag import Dag
from tdp.core.service_manager import ServiceManager

from tdp_server.api.openid_dependencies import validate_token
from tdp_server.core.config import settings
from tdp_server.db.session import SessionLocal

COMMON_RESPONSES = {
    401: {
        "description": "Unauthenticated",
        "content": {
            "application/json": {
                "example": {"detail": "Error during authentication validation (reason)"}
            }
        },
    },
    403: {
        "description": "Not enough privileges",
        "headers": {
            "WWW-Authenticate": {
                "schema": {"type": "string"},
                "description": "Authentication method to use",
            }
        },
        "content": {
            "application/json": {"example": {"detail": "Not enough permissions"}}
        },
    },
}


def get_db() -> Generator:
    with SessionLocal() as db:
        yield db


@lru_cache()
def get_dag() -> Dag:
    return Dag()


@lru_cache()
def get_service_managers(dag: Dag = Depends(get_dag)) -> Dict[str, ServiceManager]:
    return ServiceManager.get_service_managers(dag, settings.TDP_VARS)


async def read_protected(
    _=Security(validate_token, scopes=[settings.SCOPE_NAMESPACE + ":read"])
):
    pass


async def write_protected(
    _=Security(validate_token, scopes=[settings.SCOPE_NAMESPACE + ":write"])
):
    pass


async def execute_protected(
    _=Security(validate_token, scopes=[settings.SCOPE_NAMESPACE + ":execute"])
):
    pass
