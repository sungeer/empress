from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

from src import settings
from src.core.context import new_trace_id


def _with_trace(job_id, func):
    # 每次任务执行生成唯一 trace_id，作用域内日志自动带上；闭包不可 pickle，
    # 但当前 job 不持久化（纯内存 add_job），故可用
    def wrapper(*args, **kwargs):
        trace_id = new_trace_id(job_id)
        with logger.contextualize(trace_id=trace_id):
            return func(*args, **kwargs)
    return wrapper


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
