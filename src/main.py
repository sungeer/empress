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
    """Python 默认只把 SIGINT 转成 KeyboardInterrupt
    SIGTERM 不处理会直接终止进程
    """
    raise KeyboardInterrupt


def run():
    setup_logger()

    httpx.init()

    try:
        scheduler = build_scheduler()
        register_jobs(scheduler)
        scheduler.start()
    except Exception:
        logger.exception('scheduler failed to start')
        raise

    logger.info('scheduler started: %d jobs', len(scheduler.get_jobs()))

    signal.signal(signal.SIGTERM, _on_sigterm)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        logger.info('scheduler shutdown')

        # scheduler.shutdown()

        httpx.close()

        os._exit(0)


if __name__ == '__main__':
    run()
