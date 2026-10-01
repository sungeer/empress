import logging

logger = logging.getLogger(__name__)


# 定点任务 每天 02:00 跑一次
def daily_cleanup():
    logger.info('run daily_cleanup')
