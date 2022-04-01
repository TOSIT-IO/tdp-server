from tdp.core.models import ActionLog, Base, DeploymentLog, ServiceLog

from tdp_server.core.config import settings

Base.metadata.schema = settings.POSTGRES_SCHEMA
