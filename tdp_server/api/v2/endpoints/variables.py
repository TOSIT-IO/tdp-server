from fastapi import APIRouter

from tdp_server.api.v1 import dependencies
from tdp_server.schemas.components import ComponentUpdateResponse
from tdp_server.schemas.services import ServiceUpdateResponse, ServiceSchema
from tdp_server.schemas.variables import Variables, VariableValidation

router = APIRouter()


@router.get(
    "/validate",
    response_model=VariableValidation,
    responses={**dependencies.COMMON_RESPONSES},
)
def get_validate():
    """
    Validates service and component variables.
    """
    raise NotImplementedError


@router.get(
    "/{service_id}",
    response_model=Variables,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_service_variables(service_id: str):
    """
    Displays the service variables.
    """
    raise NotImplementedError


@router.put(
    "/{service_id}",
    response_model=ServiceUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def provide_service_variables(
    service_id: str,
    service: Variables,
):
    """
    Modifies the service variables.
    """
    raise NotImplementedError


@router.patch(
    "/{service_id}",
    response_model=ServiceUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def patch_service_variables(
    service_id: str,
    service: Variables,
):
    """
    Patch the service variables.
    """
    raise NotImplementedError


@router.get(
    "/{service_id}/schema",
    response_model=ServiceSchema,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_service_schema(service_id: str):
    """
    Displays the service schema.
    """
    raise NotImplementedError


@router.get(
    "/{service_id}/components/{component_id}",
    response_model=Variables,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_component_variables(service_id: str, component_id: str):
    """
    Displays the component variables.
    """
    raise NotImplementedError


@router.put(
    "/{service_id}/components/{component_id}",
    response_model=ComponentUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def provide_component_variables(
    service_id: str, component_id: str, component: Variables
):
    """
    Modifies the component variables.
    """
    raise NotImplementedError


@router.patch(
    "/{service_id}/components/{component_id}",
    response_model=ComponentUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def patch_component_variables(service_id: str, component_id: str, component: Variables):
    """
    Patches the component variables.
    """
    raise NotImplementedError
