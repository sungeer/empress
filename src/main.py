from src import tasks
from src.core.logger import setup_logger
from src.core.scheduler import build_scheduler


def run():
    setup_logger()

    scheduler = build_scheduler()

    for job_id, func, kwargs in tasks.JOBS:
        scheduler.add_job(func, id=job_id, replace_existing=True, **kwargs)

    try:
        scheduler.start()  # 阻塞，进程常驻
    except KeyboardInterrupt:
        scheduler.shutdown(wait=True)  # 等待正在执行的任务结束


if __name__ == '__main__':
    run()
