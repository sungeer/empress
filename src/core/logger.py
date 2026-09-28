import logging
import sys

from src import settings


def setup_logger():
    root = logging.getLogger()

    if root.handlers:
        return

    logging.addLevelName(logging.DEBUG, 'DBG')
    logging.addLevelName(logging.INFO, 'INF')
    logging.addLevelName(logging.WARNING, 'WRN')
    logging.addLevelName(logging.ERROR, 'ERR')
    logging.addLevelName(logging.CRITICAL, 'CRT')

    logging.getLogger('apscheduler').setLevel(logging.WARNING)

    root.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)s | %(message)s (%(name)s:%(lineno)d)',
        datefmt='%H:%M:%S'
    )

    if settings.ENVIRONMENT == 'development':
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root.addHandler(console_handler)

    log_file = settings.LOG_DIR / 'empress.log'

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)
