from datetime import datetime, timezone
from typing import Optional

from tdp.core.models import DeploymentLog

from tdp_server.schemas import DeploymentLog


def to_utc_datetime(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc)


def to_optional_utc_datetime(dt: Optional[datetime]) -> Optional[datetime]:
    if dt is not None:
        to_utc_datetime(dt)
    return dt


def deployment_from_deployment_log(deployment_log: DeploymentLog, user: str):
    return DeploymentLog(
        id=deployment_log.id,  # type: ignore
        sources=deployment_log.sources,  # type: ignore
        targets=deployment_log.targets,  # type: ignore
        filter_expression=deployment_log.filter_expression,  # type: ignore
        start_time=to_utc_datetime(deployment_log.start_time),  # type: ignore
        end_time=to_optional_utc_datetime(deployment_log.end_time),  # type: ignore
        restart=deployment_log.restart,  # type: ignore
        state=deployment_log.state,  # type: ignore
        operations=list(map(lambda op: op.operation, deployment_log.operations)),
        user=user,
    )
