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

DAG = Dag()
SERVICE_MANAGERS = ServiceManager.get_service_managers(DAG, settings.TDP_VARS)

def get_db() -> Generator:
    with SessionLocal() as db:
        yield db


def get_dag() -> Dag:
    return DAG


def get_service_managers() -> Dict[str, ServiceManager]:
    return SERVICE_MANAGERS


async def read_protected(
    user_info=Security(validate_token, scopes=[settings.SCOPE_NAMESPACE + ":read"])
) -> str:
    return user_info["sub"]


async def write_protected(
    user_info=Security(validate_token, scopes=[settings.SCOPE_NAMESPACE + ":write"])
) -> str:
    return user_info["sub"]


async def execute_protected(
    user_info=Security(validate_token, scopes=[settings.SCOPE_NAMESPACE + ":execute"])
) -> str:
    return user_info["sub"]
