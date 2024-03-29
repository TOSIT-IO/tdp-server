from pathlib import Path

from tdp.core import models as tdp_models

from alembic import command
from alembic.config import Config
from tdp_server import models
from tdp_server.core.config import settings
from tdp_server.db.base import Base
from tdp_server.db.session import engine

Base.metadata.create_all(engine)

alembic_cfg = Config(str(Path(__file__).parent / ".." / "alembic.ini"))
command.stamp(alembic_cfg, "head")
