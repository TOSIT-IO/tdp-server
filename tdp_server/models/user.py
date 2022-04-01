from sqlalchemy import Column, Integer

from tdp_server.db.base import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
