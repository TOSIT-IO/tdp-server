from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tdp_server.core.config import settings

engine = create_engine(settings.DATABASE_DSN, pool_pre_ping=True, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
