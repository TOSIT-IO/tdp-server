from typing import List

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from tdp_server.db.base import DeploymentLog as tdp_DeploymentLog
from tdp_server.db.base import OperationLog as tdp_OperationLog
from tdp_server.models import UserDeploymentLog
from tdp_server.schemas import DeploymentLog, DeploymentLogWithOperations, OperationLog

from .utils import parse_deployment_log


class DeploymentCrud:
    @staticmethod
    def get_deployments(db: Session, limit: int, offset: int) -> List[DeploymentLog]:
        query = (
            select(tdp_DeploymentLog)
            .outerjoin(UserDeploymentLog)
            .order_by(tdp_DeploymentLog.id)
            .limit(limit)
            .offset(offset)
        )
        query_result = db.execute(query).unique().scalars().fetchall()

        return [
            parse_deployment_log(deployment_log, DeploymentLog)
            for deployment_log in query_result
        ]

    @staticmethod
    def get_deployment(db: Session, deployment_id: int) -> DeploymentLogWithOperations:
        query = (
            select(tdp_DeploymentLog)
            .outerjoin(UserDeploymentLog)
            .where(tdp_DeploymentLog.id == deployment_id)
        )
        try:
            deployment_log = db.execute(query).scalar_one()
        except NoResultFound:
            raise ValueError("Invalid deployment id")
        deployment_schema = parse_deployment_log(
            deployment_log, DeploymentLogWithOperations
        )
        return deployment_schema

    @staticmethod
    def get_deployment_operation(
        db: Session, deployment_id: int, operation: str
    ) -> OperationLog:
        query = (
            select(tdp_OperationLog)
            .where(tdp_OperationLog.deployment_id == deployment_id)
            .where(tdp_OperationLog.operation == operation)
        )
        try:
            operation_log = db.execute(query).scalar_one()
        except NoResultFound:
            raise ValueError("Invalid deployment id or operation name")

        return OperationLog.from_orm(operation_log)
