from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tdp_server.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,  # type: ignore
    pool_pre_ping=True,
    connect_args={"options": f"-csearch_path={settings.POSTGRES_SCHEMA}"},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
