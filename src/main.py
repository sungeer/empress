import logging
import os
import signal
import time

from src.core.logger import setup_logger
from src.core.http_client import httpx
from src.core.scheduler import build_scheduler
from src.jobs import register_jobs

logger = logging.getLogger(__name__)


# noinspection PyUnusedLocal
def _on_sigterm(signum, frame):
    raise KeyboardInterrupt


def run():
    setup_logger()

    signal.signal(signal.SIGTERM, _on_sigterm)  # linux
    signal.signal(signal.SIGINT, _on_sigterm)  # windows

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
            time.sleep(0.1)
    except KeyboardInterrupt:
        logger.info('scheduler shutdown')

        # scheduler.shutdown(wait=True)  # 等待正在执行的任务结束

        os._exit(0)
