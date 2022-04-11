from typing import Any, Mapping, Optional, Tuple

from tdp.core.repository.git_repository import GitRepository
from tdp.core.service_manager import ServiceManager
from tdp_server.schemas import Variables


class VariablesCrud:
    @staticmethod
    def get_variables(
        service_manager: ServiceManager, name: Optional[str] = None
    ) -> Variables:
        filename: str = name or service_manager.name
        repository: GitRepository = service_manager.repository
        with repository.open_var_file(filename + ".yml") as configuration:
            return Variables(__root__=configuration._content)

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
        repository: GitRepository = service_manager.repository
        with repository.validate(update_message) as repo, repo.open_var_file(
            f"{filename}.yml"
        ) as service_variables:
            service_variables.update(content, merge)
        return repository.current_version(), update_message
