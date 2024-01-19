from datetime import datetime
from typing import Union
from tdp_server.schemas.deploy import DeploymentStart


class DeploymentLog(DeploymentStart):
    end_time: Union[datetime, None]
