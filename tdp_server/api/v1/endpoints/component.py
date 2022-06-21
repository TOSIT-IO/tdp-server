import logging
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from tdp.core.service_manager import ServiceManager

from tdp_server.api import dependencies
from tdp_server.schemas import Component, ComponentUpdate, ComponentUpdateResponse
from tdp_server.services import VariablesCrud

logger = logging.getLogger("tdp_server")
router = APIRouter()

COMPONENT_ID_DOES_NOT_EXISTS_ERROR = {
    400: {
        "description": "Component id does not exists",
        "content": {
            "application/json": {
                "example": {"detail": "{component_id} does not exists"}
            }
        },
    }
}


@router.get(
    "/{component_id}",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=Component,
    responses={
        **dependencies.COMMON_RESPONSES,
        **COMPONENT_ID_DOES_NOT_EXISTS_ERROR,
    },
)
def get_component(
    *,
    service_id: str,
    component_id: str,
    service_managers: Dict[str, ServiceManager] = Depends(
        dependencies.get_service_managers
    ),
) -> Any:
    """
    Gets component identified by its id
    """
    service_id = service_id.lower()
    component_id = component_id.lower()
    try:
        component = service_managers[service_id].get_component_name(component_id)
        return Component(
            id=component_id,
            variables=VariablesCrud.get_variables(
                service_managers[service_id], component
            ),
        )
    except (KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{service_id} or {component_id} does not exist.",
        )


@router.patch(
    "/{component_id}",
    response_model=ComponentUpdateResponse,
    responses={**dependencies.COMMON_RESPONSES, **COMPONENT_ID_DOES_NOT_EXISTS_ERROR},
)
def patch_component(
    *,
    service_id: str,
    component_id: str,
    component_update: ComponentUpdate,
    service_managers: Dict[str, ServiceManager] = Depends(
        dependencies.get_service_managers
    ),
    user: str = Depends(dependencies.write_protected),
) -> Any:
    """
    Modifies a component definition.
    """
    service_id = service_id.lower()
    try:
        service_manager = service_managers[service_id]
        component = service_managers[service_id].get_component_name(component_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{service_id} or {component_id} does not exist.",
        )
    update_message = component_update.message + f"\n\nuser: {user}"
    try:
        version, message = VariablesCrud.update_variables(
            service_manager,
            component_update.variables.__root__,
            update_message,
            name=component,
            merge=True,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return ComponentUpdateResponse(message=message, version=version)


@router.put(
    "/{component_id}",
    response_model=ComponentUpdateResponse,
    responses={**dependencies.COMMON_RESPONSES, **COMPONENT_ID_DOES_NOT_EXISTS_ERROR},
)
def put_component(
    *,
    service_id: str,
    component_id: str,
    component_update: ComponentUpdate,
    service_managers: Dict[str, ServiceManager] = Depends(
        dependencies.get_service_managers
    ),
    user: str = Depends(dependencies.write_protected),
) -> Any:
    """
    Sets a component definition.
    """
    service_id = service_id.lower()
    try:
        service_manager = service_managers[service_id]
        component = service_managers[service_id].get_component_name(component_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{service_id} or {component_id} does not exist.",
        )
    update_message = component_update.message + f"\n\nuser: {user}"
    try:
        version, message = VariablesCrud.update_variables(
            service_manager,
            component_update.variables.__root__,
            update_message,
            name=component,
            merge=True,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return ComponentUpdateResponse(message=message, version=version)
