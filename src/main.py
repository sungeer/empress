import signal

from src import tasks
from src.core.logger import setup_logger
from src.core.scheduler import build_scheduler


def run():
    setup_logger()

    scheduler = build_scheduler()

    for job_id, func, kwargs in tasks.JOBS:
        scheduler.add_job(func, id=job_id, replace_existing=True, **kwargs)

    def _graceful_shutdown(_signum, _frame):
        # 收到 SIGTERM/SIGINT 时优雅退出：等待正在执行的任务结束
        scheduler.shutdown(wait=True)

    signal.signal(signal.SIGTERM, _graceful_shutdown)
    signal.signal(signal.SIGINT, _graceful_shutdown)

    scheduler.start()  # 阻塞，进程常驻


if __name__ == '__main__':
    run()
