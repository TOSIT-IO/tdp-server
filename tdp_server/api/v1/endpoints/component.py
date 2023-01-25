import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from tdp.core.dag import Dag
from tdp.core.variables import ClusterVariables, ServiceVariables

from tdp_server.api import dependencies
from tdp_server.schemas import Component, ComponentUpdate, ComponentUpdateResponse
from tdp_server.services import VariablesCrud

logger = logging.getLogger("tdp_server")
router = APIRouter()


@router.get(
    "/{component_id}",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=Component,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_component(
    component_id: str,
    *,
    service: ServiceVariables = Depends(dependencies.service),
    dag: Dag = Depends(dependencies.get_dag),
) -> Any:
    """
    Gets component identified by its id
    """
    component_id = component_id.lower()
    try:
        version = service.version
        component = service.get_component_name(dag, component_id)
        return Component(
            id=component_id,
            service_id=service.name,
            variables=VariablesCrud.get_variables(service, component),
            version=version,
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{component_id} does not exist.",
        )


@router.patch(
    "/{component_id}",
    response_model=ComponentUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def patch_component(
    component_id: str,
    component_update: ComponentUpdate,
    *,
    service: ServiceVariables = Depends(dependencies.service),
    dag: Dag = Depends(dependencies.get_dag),
    user: str = Depends(dependencies.write_protected),
) -> Any:
    """
    Modifies a component definition.
    """
    try:
        component = service.get_component_name(dag, component_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{component_id} does not exist.",
        )
    update_message = component_update.message + f"\n\nuser: {user}"
    try:
        version, message = VariablesCrud.update_variables(
            service,
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
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.COMPONENT_ID_DOES_NOT_EXIST_ERROR,
    },
)
def put_component(
    component_id: str,
    component_update: ComponentUpdate,
    *,
    service: ServiceVariables = Depends(dependencies.service),
    dag: Dag = Depends(dependencies.get_dag),
    user: str = Depends(dependencies.write_protected),
) -> Any:
    """
    Sets a component definition.
    """
    try:
        component = service.get_component_name(dag, component_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{component_id} does not exist.",
        )
    update_message = component_update.message + f"\n\nuser: {user}"
    try:
        version, message = VariablesCrud.update_variables(
            service,
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
