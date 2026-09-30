import logging
import os
import signal
import time

from src.core.logger import setup_logger
from src.core.http_client import httpx
from src.core.scheduler import build_scheduler
from src.jobs import register_jobs

logger = logging.getLogger(__name__)


def _on_sigterm(signum, frame):
    raise KeyboardInterrupt


def run():
    setup_logger()

    signal.signal(signal.SIGTERM, _on_sigterm)

    httpx.init()

    try:
        scheduler = build_scheduler()
        register_jobs(scheduler)

        logger.info('registered %d jobs', len(scheduler.get_jobs()))

        scheduler.start()

        logger.info('scheduler started')
    except Exception:
        logger.exception('scheduler failed to start')
        raise

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info('scheduler shutdown')

        os._exit(0)
