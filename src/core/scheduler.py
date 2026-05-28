from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor

scheduler = BackgroundScheduler(
    executors={
        'io_tasks': ThreadPoolExecutor(max_workers=20)，
        'cpu_tasks': ThreadPoolExecutor(max_workers=5)
    }
)
