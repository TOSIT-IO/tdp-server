from typing import Any, Mapping, Optional, Tuple

from tdp.core.repository.repository import EmptyCommit
from tdp.core.service_manager import ServiceManager

from tdp_server.schemas import Variables


class VariablesCrud:
    @staticmethod
    def get_variables(
        service_manager: ServiceManager, name: Optional[str] = None
    ) -> Variables:
        filename: str = name or service_manager.name
        repository = service_manager.repository
        try:
            with repository.open_var_file(
                filename + ".yml", fail_if_does_not_exist=True
            ) as configuration:
                return Variables(__root__=configuration.copy())
        except ValueError:
            return Variables(__root__={})

    @staticmethod
    def update_variables(
        service_manager: ServiceManager,
        content: Mapping[str, Any],
        message: str,
        name: Optional[str] = None,
        merge: bool = True,
    ) -> Tuple[str, str]:
        filename: str = name or service_manager.name

        update_message = f"[{service_manager.name}] {message}"
        repository = service_manager.repository
        try:
            with repository.validate(update_message) as repo, repo.open_var_file(
                f"{filename}.yml"
            ) as service_variables:
                if merge:
                    service_variables.merge(content)
                else:
                    service_variables.clear()
                    service_variables.update(content)
        except EmptyCommit as e:
            raise ValueError(e)
        return repository.current_version(), update_message
