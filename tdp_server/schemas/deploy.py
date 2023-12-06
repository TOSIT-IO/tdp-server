from typing import Optional

from tdp_server.schemas.common import CommonOptions


class DeployOptions(CommonOptions):
    force_stale_update: Optional[bool] = False
    dry: Optional[bool] = False
    mock_deploy: Optional[bool] = False
    run_directory: Optional[str]
