from typing import Any, Mapping, Optional, Tuple

import jsonschema
from jsonschema.exceptions import ValidationError
from tdp.core.repository.repository import EmptyCommit
from tdp.core.variables import ServiceVariables, VariablesDict
from tdp.core.variables.service_variables import YML_EXTENSION, CustomValidator

from tdp_server.schemas import Variables


class VariablesCrud:
    @staticmethod
    def get_variables(
        service: ServiceVariables, name: Optional[str] = None
    ) -> Variables:
        filename: str = name or service.name
        variables = service.get_variables(filename)
        return Variables(__root__=variables or {})

    @staticmethod
    def update_variables(
        service: ServiceVariables,
        content: Mapping[str, Any],
        message: str,
        name: Optional[str] = None,
        merge: bool = True,
    ) -> Tuple[str, str]:
        service_or_component: str = name or service.name
        is_service = name == service.name
        validate_schema(service, content, merge, service_or_component, is_service)
        try:
            filename = service_or_component + YML_EXTENSION
            with service.open_var_files(message, [filename]) as configurations:
                service_configuration = configurations[filename]
                if merge:
                    service_configuration.merge(content)
                else:
                    service_configuration.clear()
                    service_configuration.update(content)
        except EmptyCommit as e:
            raise ValueError(e)
        return service.version, message


def validate_schema(
    service: ServiceVariables,
    content: Mapping[str, Any],
    merge: bool,
    service_or_component,
    is_service: bool,
):
    to_check = VariablesDict(service.get_variables(service.name))

    if is_service:
        if merge:
            to_check.merge(content)
        else:
            to_check = VariablesDict(content)
    else:
        if merge:
            component_vars = VariablesDict(service.get_variables(service_or_component))
            to_check.merge(component_vars)
        to_check.merge(content)
    try:
        jsonschema.validate(to_check, service.schema, CustomValidator)
    except ValidationError as e:
        raise ValueError(str(e))
