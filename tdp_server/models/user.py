import uuid

from sqlalchemy import Boolean, Column, Integer, String

from tdp_server.db.base import Base


def gen_uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "user"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    access_token = Column(String(length=4096), nullable=False)
    expires_at = Column(Integer, nullable=True)
    refresh_token = Column(String(length=4096), nullable=True)
    account_id = Column(String(256), index=True, nullable=False, unique=True)
    account_email = Column(String(256), nullable=False)
    read = Column(Boolean, default=False, nullable=False)
    write = Column(Boolean, default=False, nullable=False)
    execute = Column(Boolean, default=False, nullable=False)
