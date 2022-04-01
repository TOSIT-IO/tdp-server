import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from tdp.core.dag import Dag
from tdp.core.repository.git_repository import GitRepository
from tdp.core.service_manager import ServiceManager

from tdp_server.api import dependencies
from tdp_server.schemas import Component, Service, ServiceUpdate
from tdp_server.schemas.service import ServiceUpdateResponse

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
) -> Any:
    """
    Returns the list of services
    """
    services = []
    for service, service_components in dag.services_components.items():
        services.append(
            Service(
                id=service,
                components=[
                    Component(id=component.name) for component in service_components
                ],
            )
        )
    return services


@router.get(
    "/{service_id}",
    dependencies=[Depends(dependencies.read_protected)],
    response_model=Service,
    responses={
        **dependencies.COMMON_RESPONSES,
        400: {
            "description": "Service id provided does not exists",
            "content": {
                "application/json": {
                    "example": {"detail": "{service_id} does not exists"}
                }
            },
        },
    },
)
def get_service(
    *,
    service_id: str,
    dag: Dag = Depends(dependencies.get_dag),
) -> Any:
    """
    Gets service identified by its id
    """
    service_id = service_id.lower()
    try:
        components = dag.services_components[service_id]
        return Service(
            id=service_id,
            components=[Component(id=component.name) for component in components],
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{service_id} does not exist.",
        )


@router.patch(
    "/{service_id}",
    dependencies=[Depends(dependencies.write_protected)],
    response_model=ServiceUpdateResponse,
    responses={**dependencies.COMMON_RESPONSES},
)
def patch_service(
    *,
    service_id: str,
    service_update: ServiceUpdate,
    service_managers: Dict[str, ServiceManager] = Depends(
        dependencies.get_service_managers
    ),
):
    """
    Modifies a service definition.
    """
    service_id = service_id.lower()
    try:
        service_manager = service_managers[service_id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{service_id} does not exist.",
        )
    update_message = f"[{service_id}] {service_update.message}"
    repository: GitRepository = service_manager.repository
    try:
        with repository.validate(update_message) as repo, repo.open_var_file(
            f"{service_id}.yml"
        ) as service_variables:
            service_variables.update(service_update.variables.__root__)
        version = repository.current_version()
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return {"message": update_message, "version": version}


@router.put(
    "/{service_id}",
    dependencies=[Depends(dependencies.write_protected)],
    response_model=Service,
    responses={**dependencies.COMMON_RESPONSES},
)
def put_service(
    *,
    service_id: str,
    service_update: ServiceUpdate,
    dag: Dag = Depends(dependencies.get_dag),
) -> Any:
    """
    Sets a service definition.
    """
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
