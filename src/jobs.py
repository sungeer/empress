from src.core.scheduler import scheduler
from src.domains.health.jobs import register_jobs as register_health_jobs


def setup_all_jobs():
    register_health_jobs(scheduler)
