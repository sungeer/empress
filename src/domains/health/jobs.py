from src.domains.health import repository
from src.core.db_registry import db


def check_db_conn():
    with db.connect() as cursor:
        repository.check_db_conn(cursor)

    return None


def register_jobs(scheduler):
    scheduler.add_job(check_db_conn, 'interval', seconds=60, id='haiku.some_job')
