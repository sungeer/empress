import time

from src import tasks
from src.core.logger import setup_logger
from src.core.scheduler import build_scheduler


def run():
    setup_logger()

    scheduler = build_scheduler()

    for job_id, func, kwargs in tasks.JOBS:
        scheduler.add_job(
            func,
            id=job_id,
            replace_existing=True,
            **kwargs
        )

    scheduler.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        scheduler.shutdown()


if __name__ == '__main__':
    run()
