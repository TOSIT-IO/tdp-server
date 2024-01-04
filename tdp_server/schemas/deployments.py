from datetime import datetime

from tdp_server.schemas.deploy import DeploymentStart


class DeploymentLog(DeploymentStart):
    end_time: datetime
