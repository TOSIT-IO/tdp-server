import logging
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from tdp.core.dag import Dag
from tdp.core.variables import ClusterVariables, ServiceVariables

from tdp_server.api import dependencies
from tdp_server.schemas import Component, Service, ServiceUpdate, ServiceUpdateResponse
from tdp_server.services import VariablesCrud

logger = logging.getLogger("tdp_server")
router = APIRouter()


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
                        service_id=service.name,
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
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def get_service(
    *,
    service: ServiceVariables = Depends(dependencies.service),
    dag: Dag = Depends(dependencies.get_dag),
) -> Any:
    """
    Gets service identified by its id
    """
    operations = dag.services_operations[service.name]
    components = {
        operation.component for operation in operations if operation.component
    }
    version = service.version
    return Service(
        id=service.name,
        components=[
            Component(
                id=component,
                service_id=service.name,
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


@router.patch(
    "/{service_id}",
    response_model=ServiceUpdateResponse,
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def patch_service(
    service_update: ServiceUpdate,
    *,
    service: ServiceVariables = Depends(dependencies.service),
    user: str = Depends(dependencies.write_protected),
) -> Any:
    """
    Modifies a service definition.
    """
    update_message = service_update.message + f"\n\nuser: {user}"
    try:
        version, message = VariablesCrud.update_variables(
            service,
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
    responses={
        **dependencies.COMMON_RESPONSES,
        **dependencies.SERVICE_ID_DOES_NOT_EXIST_ERROR,
    },
)
def put_service(
    service_update: ServiceUpdate,
    *,
    service: ServiceVariables = Depends(dependencies.service),
    user: str = Depends(dependencies.write_protected),
) -> Any:
    """
    Sets a service definition.
    """
    update_message = service_update.message + f"\n\nuser: {user}"
    try:
        version, message = VariablesCrud.update_variables(
            service,
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
