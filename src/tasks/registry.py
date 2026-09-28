from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from src.tasks.cleanup import daily_cleanup
from src.tasks.example import task_a, task_b, task_c


def register_jobs(scheduler):
    scheduler.add_job(
        task_a, id='task_a',
        replace_existing=True,
        trigger=IntervalTrigger(minutes=1)
    )
    scheduler.add_job(
        task_b, id='task_b',
        replace_existing=True,
        trigger=IntervalTrigger(minutes=2)
    )
    scheduler.add_job(
        task_c, id='task_c',
        replace_existing=True,
        trigger=IntervalTrigger(minutes=3)
    )
    scheduler.add_job(
        daily_cleanup, id='daily_cleanup',
        replace_existing=True,
        trigger=CronTrigger(hour=2, minute=0)
    )
