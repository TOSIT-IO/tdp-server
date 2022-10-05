from typing import Any, Mapping, Optional, Tuple

from tdp.core.repository.repository import EmptyCommit
from tdp.core.variables import ServiceVariables

from tdp_server.schemas import Variables


class VariablesCrud:
    @staticmethod
    def get_variables(
        service_variables: ServiceVariables, name: Optional[str] = None
    ) -> Variables:
        filename: str = name or service_variables.name
        variables = service_variables.get_variables(filename)
        return Variables(__root__=variables or {})

    @staticmethod
    def update_variables(
        service_variables: ServiceVariables,
        content: Mapping[str, Any],
        message: str,
        name: Optional[str] = None,
        merge: bool = True,
    ) -> Tuple[str, str]:
        filename: str = name or service_variables.name
        try:
            with service_variables.open_var_files(
                message, [f"{filename}.yml"]
            ) as configurations:
                service_configuration = configurations[f"{filename}.yml"]
                if merge:
                    service_configuration.merge(content)
                else:
                    service_configuration.clear()
                    service_configuration.update(content)
        except EmptyCommit as e:
            raise ValueError(e)
        return service_variables.version, message
