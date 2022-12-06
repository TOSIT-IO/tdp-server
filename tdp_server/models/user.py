from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)
from sqlalchemy import Column, Integer, String

from tdp_server.db.base import Base

# https://openid.net/specs/openid-connect-core-1_0.html#IDToken
# sub field is maximum 255 characters
SUB_MAX_SIZE = 255

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    sub = Column(String(SUB_MAX_SIZE), unique=True)
