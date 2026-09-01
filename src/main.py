import os
import signal

from loguru import logger

from src import tasks
from src.core.context import new_trace_id
from src.core.logger import setup_logger
from src.core.scheduler import build_scheduler


def with_trace(func, *args, **kwargs):
    with logger.contextualize(trace_id=new_trace_id()):
        return func(*args, **kwargs)


def run():
    setup_logger()

    scheduler = build_scheduler()

    for job_id, func, kwargs in tasks.JOBS:
        # scheduler.add_job(func, id=job_id, replace_existing=True, **kwargs)
        scheduler.add_job(
            with_trace, id=job_id, replace_existing=True,
            args=[func], **kwargs,
        )

    def _stop(_signum, _frame):
        # 收到 SIGTERM/SIGINT 立即退出，不等正在执行的任务
        os._exit(0)

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    scheduler.start()  # 阻塞，进程常驻


if __name__ == '__main__':
    run()
