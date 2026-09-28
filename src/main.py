import logging
import os
import time

from src.core.logger import setup_logger
from src.core.scheduler import build_scheduler
from src.jobs import register_jobs

logger = logging.getLogger(__name__)


def run():
    setup_logger()

    try:
        scheduler = build_scheduler()
        register_jobs(scheduler)
        scheduler.start()
    except Exception:
        logger.exception('scheduler failed to start')
        raise

    logger.info('scheduler started: %d jobs', len(scheduler.get_jobs()))

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        logger.info('scheduler shutdown')
        # scheduler.shutdown()
        os._exit(0)


if __name__ == '__main__':
    run()
