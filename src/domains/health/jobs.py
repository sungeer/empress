from loguru import logger

from src.domains.health import repository
from src.core.db_registry import db

logger.add(
      'logs/cron/sync_users.log',
      rotation='50 MB',
      retention=3,
      format='{time:YYYY-MM-DD HH:mm:ss} - {level} - [{extra[run_id]}] {name}:{function}:{line} -
  {message}',
      encoding='utf-8',
      enqueue=True,
      level='INFO',
      filter=lambda r: r['extra'].get('task') == 'sync_users',
  )

  log = logger.bind(task='sync_users')


def check_db_conn():
    log.info('开始同步用户数据...')
    with db.connect() as cursor:
        repository.check_db_conn(cursor)

    return None


def register_jobs(scheduler):
    scheduler.add_job(check_db_conn, 'interval', seconds=60, id='haiku.some_job', executor='io_tasks')
    # scheduler.add_job(cpu_intensive_task, 'cron', hour=2, executor='cpu_tasks')
