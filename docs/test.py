# src/scheduler_service.py
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src import tasks  # 10 个任务函数，必须全局可 import


def _build_scheduler() -> BlockingScheduler:
    return BlockingScheduler(
        executors={
            'default': ThreadPoolExecutor(20),  # 10 个任务可互相并行
        },
        job_defaults={
            'max_instances': 1,  # 关键：到点若还在跑，本次跳过
            'coalesce': True,  # 若真错过多次，只补最后一次
            'misfire_grace_time': 60,  # 触发延迟超 1 分钟才视为错过
        },
        timezone='Asia/Shanghai',
    )


def main():
    scheduler = _build_scheduler()

    # 每隔 3 分钟的任务（10 个同理）
    for task in (tasks.task_a, tasks.task_b, tasks.task_c):
        scheduler.add_job(
            task,
            IntervalTrigger(minutes=3),
            id=task.__name__,
            replace_existing=True,
        )

    # 固定时间点任务
    scheduler.add_job(
        tasks.daily_cleanup,
        'cron',
        hour=2,
        minute=0,
        id='daily_cleanup',
        replace_existing=True,
    )

    scheduler.start()  # 阻塞，进程常驻


if __name__ == '__main__':
    main()
