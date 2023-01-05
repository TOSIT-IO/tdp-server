import time

from authlib.integrations.sqla_oauth2 import (
    OAuth2AuthorizationCodeMixin,
    OAuth2ClientMixin,
    OAuth2TokenMixin,
)
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from tdp_server.db.base import Base


class OAuth2Client(Base, OAuth2ClientMixin):
    __tablename__ = "oauth2_client"

    id = Column(Integer, primary_key=True)


class OAuth2AuthorizationCode(Base, OAuth2AuthorizationCodeMixin):
    __tablename__ = "oauth2_code"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User")

    def is_expired(self):
        return self.auth_time + 300 < time.time()


class OAuth2Token(Base, OAuth2TokenMixin):
    __tablename__ = "oauth2_token"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User")

    def is_refresh_token_active(self):
        """Check if refresh token is active"""
        if self.revoked:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()
