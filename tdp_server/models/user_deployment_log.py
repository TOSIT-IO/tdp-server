from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from tdp_server.db.base import Base



class UserDeploymentLog(Base):
    __tablename__ = "user_deployment_log"

    deployment_id = Column(ForeignKey("deployment_log.id"), primary_key=True)
    user_identifier = Column(ForeignKey("user.sub"))
    deployment = relationship(
        "DeploymentLog", backref=backref("user_deployment_log", uselist=False)
    )
