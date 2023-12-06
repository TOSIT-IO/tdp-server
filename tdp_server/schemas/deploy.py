from pydantic import BaseModel
from typing import Optional, List


class DeployOptions(BaseModel):
    collections: List[str]
    database_dsn: str
    force_stale_update: Optional[bool] = False
    dry: Optional[bool] = False
    mock_deploy: Optional[bool] = False
    validate: Optional[bool] = False
    run_directory: str
    variables: str
