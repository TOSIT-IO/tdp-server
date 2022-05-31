from tdp.core.dag import Dag
from tdp.core.service_manager import ServiceManager

from tdp_server.core.config import settings

ServiceManager.initialize_service_managers(
    Dag.from_collections(settings.TDP_COLLECTIONS),
    settings.TDP_VARS,
)
