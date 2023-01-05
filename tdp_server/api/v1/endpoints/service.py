import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from tdp.core.dag import Dag
from tdp.core.variables import ClusterVariables

from tdp_server.api import dependencies
from tdp_server.schemas import Component, Service, ServiceUpdate, ServiceUpdateResponse
from tdp_server.services import VariablesCrud

logger = logging.getLogger("tdp_server")
router = APIRouter()

SERVICE_ID_DOES_NOT_EXISTS_ERROR = {
    400: {
        "description": "Service id does not exists",
        "content": {
            "application/json": {"example": {"detail": "{service_id} does not exists"}}
        },
    }
}


@router.get(
    "/",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=List[Service],
    responses={**dependencies.COMMON_RESPONSES},
)
def get_services(
    *,
    dag: Dag = Depends(dependencies.get_dag),
    cluster_variables: ClusterVariables = Depends(dependencies.get_cluster_variables),
) -> Any:
    """
    Returns the list of services
    """
    services = []
    for service_name, service_operations in dag.services_operations.items():
        service = cluster_variables[service_name]
        version = service.version
        components = {
            operation.component
            for operation in service_operations
            if operation.component
        }
        services.append(
            Service(
                id=service_name,
                components=[
                    Component(
                        id=component,
                        variables=VariablesCrud.get_variables(
                            service, service.name + "_" + component
                        ),
                        version=version,
                    )
                    for component in components
                ],
                variables=VariablesCrud.get_variables(service),
                version=version,
            )
        )
    return services


@router.get(
    "/{service_id}",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=Service,
    responses={
        **dependencies.COMMON_RESPONSES,
        **SERVICE_ID_DOES_NOT_EXISTS_ERROR,
    },
)
def get_service(
    *,
    service_id: str,
    dag: Dag = Depends(dependencies.get_dag),
    cluster_variables: ClusterVariables = Depends(dependencies.get_cluster_variables),
) -> Any:
    """
    Gets service identified by its id
    """
    service_id = service_id.lower()
    try:
        operations = dag.services_operations[service_id]
        components = {
            operation.component for operation in operations if operation.component
        }
        service = cluster_variables[service_id]
        version = service.version
        return Service(
            id=service_id,
            components=[
                Component(
                    id=component,
                    variables=VariablesCrud.get_variables(
                        service, service.name + "_" + component
                    ),
                    version=version,
                )
                for component in components
            ],
            variables=VariablesCrud.get_variables(service),
            version=version,
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{service_id} does not exist.",
        )


@router.patch(
    "/{service_id}",
    response_model=ServiceUpdateResponse,
    responses={**dependencies.COMMON_RESPONSES, **SERVICE_ID_DOES_NOT_EXISTS_ERROR},
)
def patch_service(
    *,
    service_id: str,
    service_update: ServiceUpdate,
    cluster_variables: ClusterVariables = Depends(dependencies.get_cluster_variables),
    user: str = Depends(dependencies.write_protected),
) -> Any:
    """
    Modifies a service definition.
    """
    service_id = service_id.lower()
    try:
        service_manager = cluster_variables[service_id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{service_id} does not exist.",
        )
    update_message = service_update.message + f"\n\nuser: {user}"
    try:
        version, message = VariablesCrud.update_variables(
            service_manager,
            service_update.variables.__root__,
            update_message,
            merge=True,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return ServiceUpdateResponse(message=message, version=version)


@router.put(
    "/{service_id}",
    response_model=ServiceUpdateResponse,
    responses={**dependencies.COMMON_RESPONSES, **SERVICE_ID_DOES_NOT_EXISTS_ERROR},
)
def put_service(
    *,
    service_id: str,
    service_update: ServiceUpdate,
    cluster_variables: ClusterVariables = Depends(dependencies.get_cluster_variables),
    user: str = Depends(dependencies.write_protected),
) -> Any:
    """
    Sets a service definition.
    """
    service_id = service_id.lower()
    try:
        service_manager = cluster_variables[service_id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{service_id} does not exist.",
        )
    update_message = service_update.message + f"\n\nuser: {user}"
    try:
        version, message = VariablesCrud.update_variables(
            service_manager,
            service_update.variables.__root__,
            update_message,
            merge=False,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return ServiceUpdateResponse(message=message, version=version)
