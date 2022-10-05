from tdp.core.variables import ClusterVariables

from tdp_server.core.config import settings

ClusterVariables.initialize_cluster_variables(
    settings.TDP_COLLECTIONS,
    settings.TDP_VARS,
)
