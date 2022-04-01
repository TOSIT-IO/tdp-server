import logging

from tdp_server.core.config import settings


def init_loggers():
    logger = logging.getLogger("tdp_server")
    logger.setLevel(settings.LOG_LEVEL)
