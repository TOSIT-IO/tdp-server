from typing import Type, TypeVar

from pydantic import parse_obj_as
from tdp.core.models import DeploymentLog as tdp_DeploymentLog
from tdp.core.operation import Operation as tdp_Operation

from tdp_server.schemas import DeploymentLog, Operation

D = TypeVar("D", bound=DeploymentLog)


def operation_schema_from_operation(operation: tdp_Operation) -> Operation:
    return parse_obj_as(Operation, operation.__dict__)


def parse_deployment_log(
    deployment_log: tdp_DeploymentLog, schema_class: Type[D], user=None
) -> D:
    deployment_schema = schema_class.from_orm(deployment_log)
    if user is not None:
        deployment_schema.user = user
    if deployment_log.user_deployment_log is not None:
        deployment_schema.user = deployment_log.user_deployment_log.user_identifier
    return deployment_schema
