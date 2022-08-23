from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session
from tdp.core.runner.executor import StateEnum

from tdp_server.db.base import DeploymentLog, OperationLog
from tdp_server.models import UserDeploymentLog
from tdp_server.schemas import Deployment, DeploymentWithOperations, Operation

NO_USER = "NO_USER_RECORDED"


def user_or_not(deployment_log) -> str:
    if deployment_log.user_deployment_log is None:
        return NO_USER
    return deployment_log.user_deployment_log.user


class DeploymentCrud:
    @staticmethod
    def get_deployments(db: Session, limit: int, offset: int) -> List[Deployment]:
        query = (
            select(DeploymentLog)
            .outerjoin(UserDeploymentLog)
            .order_by(DeploymentLog.id)
            .limit(limit)
            .offset(offset)
        )
        query_result = db.execute(query).unique().scalars().fetchall()
        print(query_result)
        return [
            Deployment(
                id=deployment_log.id,
                sources=deployment_log.sources,
                targets=deployment_log.targets,
                filter_expression=deployment_log.filter_expression,
                start_time=to_utc_datetime(deployment_log.start_time),
                end_time=to_utc_datetime(deployment_log.end_time),
                state=StateEnum(deployment_log.state),
                operations=[
                    operation.operation for operation in deployment_log.operations
                ],
                user=user_or_not(deployment_log),
            )
            for deployment_log in query_result
        ]

    @staticmethod
    def get_deployment(db: Session, deployment_id: int) -> DeploymentWithOperations:
        query = (
            select(DeploymentLog)
            .outerjoin(UserDeploymentLog)
            .where(DeploymentLog.id == deployment_id)
        )
        try:
            deployment_log = db.execute(query).scalar_one()
        except NoResultFound:
            raise ValueError("Invalid deployment id")

        return DeploymentWithOperations(
            id=deployment_log.id,
            sources=deployment_log.sources,
            targets=deployment_log.targets,
            filter_expression=deployment_log.filter_expression,
            start_time=to_utc_datetime(deployment_log.start_time),
            end_time=to_utc_datetime(deployment_log.end_time),
            state=StateEnum(deployment_log.state),
            operations=[
                Operation(
                    operation=operation_log.operation,
                    start_time=to_utc_datetime(operation_log.start_time),
                    end_time=to_utc_datetime(operation_log.end_time),
                    state=StateEnum(operation_log.state),
                    logs=operation_log.logs,
                )
                for operation_log in deployment_log.operations
            ],
            user=user_or_not(deployment_log),
        )

    @staticmethod
    def get_deployment_operation(
        db: Session, deployment_id: int, operation: str
    ) -> Operation:
        query = (
            select(OperationLog)
            .where(OperationLog.deployment_id == deployment_id)
            .where(OperationLog.operation == operation)
        )
        try:
            operation_log = db.execute(query).scalar_one()
        except NoResultFound:
            raise ValueError("Invalid deployment id or operation name")

        return Operation(
            operation=operation_log.operation,
            start_time=to_utc_datetime(operation_log.start_time),
            end_time=to_utc_datetime(operation_log.end_time),
            state=StateEnum(operation_log.state),
            logs=operation_log.logs,
        )


def to_utc_datetime(dt: Optional[datetime]):
    if dt is not None:
        dt.replace(tzinfo=timezone.utc)
    return dt
