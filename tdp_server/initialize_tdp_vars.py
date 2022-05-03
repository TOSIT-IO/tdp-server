from tdp.core.dag import Dag
from tdp.core.service_manager import ServiceManager

from tdp_server.core.config import settings

ServiceManager.initialize_service_managers(
    Dag.from_collection(settings.TDP_COLLECTION_PATH),
    settings.TDP_VARS,
    settings.TDP_COLLECTION_PATH / "tdp_vars_defaults",
)
