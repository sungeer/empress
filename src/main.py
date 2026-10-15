import logging
import os
import signal
import sys
import time

from src.core.logger import setup_logger
from src.core.http_client import httpx
from src.core.scheduler import build_scheduler
from src.jobs import register_jobs

logger = logging.getLogger(__name__)


def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    logger.critical(
        'uncaught exception',
        exc_info=(exc_type, exc_value, exc_traceback),
    )


def on_sigterm(signum, frame):  # noqa
    raise KeyboardInterrupt


def run():
    setup_logger()

    sys.excepthook = handle_uncaught_exception

    signal.signal(signal.SIGTERM, on_sigterm)  # linux
    signal.signal(signal.SIGINT, on_sigterm)  # windows

    httpx.init()

    scheduler = build_scheduler()

    register_jobs(scheduler)

    logger.info('registered %d jobs', len(scheduler.get_jobs()))

    scheduler.start()

    logger.info('scheduler started')

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        logger.info('scheduler shutdown')

        # scheduler.shutdown(wait=True)  # 等待正在执行的任务结束

        os._exit(0)
