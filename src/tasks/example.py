from loguru import logger


# 示例任务（每 3 分钟跑一次），真实业务替换函数体即可
def task_a():
    logger.info('run task_a')


def task_b():
    logger.info('run task_b')


def task_c():
    logger.info('run task_c')
