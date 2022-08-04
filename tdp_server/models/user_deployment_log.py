from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from tdp_server.db.base import Base

# https://openid.net/specs/openid-connect-core-1_0.html#IDToken
# sub field is maximum 255 characters
SUB_MAX_SIZE = 255


class UserDeploymentLog(Base):
    __tablename__ = "user_deployment_log"

    deployment_id = Column(ForeignKey("deployment_log.id"), primary_key=True)
    user = Column(String(length=SUB_MAX_SIZE))
    deployment = relationship(
        "DeploymentLog", backref=backref("user_deployment_log", uselist=False)
    )
