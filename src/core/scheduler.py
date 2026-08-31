from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler

from src import settings


def build_scheduler() -> BlockingScheduler:
    return BlockingScheduler(
        executors={
            'default': ThreadPoolExecutor(settings.TASK_WORKERS),  # 任务可互相并行
        },
        job_defaults={
            'max_instances': 1,  # 到点若还在跑，本次跳过
            'coalesce': True,  # 若真错过多次，只补最后一次
            'misfire_grace_time': settings.MISFIRE_GRACE_TIME,  # 触发延迟超过该秒数才视为错过
        },
        timezone=settings.TIMEZONE,
    )
