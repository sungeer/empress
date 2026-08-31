from apscheduler.triggers.interval import IntervalTrigger

from src.tasks.cleanup import daily_cleanup
from src.tasks.example import task_a, task_b, task_c

# 任务注册表：加任务 = 定义一个模块级函数 + 在此追加一条 (job_id, 函数, add_job 关键字参数)
# 函数必须模块级可 import（APScheduler 序列化 job 依赖函数所在模块路径）
JOBS = [
    ('task_a', task_a, {'trigger': IntervalTrigger(minutes=3)}),
    ('task_b', task_b, {'trigger': IntervalTrigger(minutes=3)}),
    ('task_c', task_c, {'trigger': IntervalTrigger(minutes=3)}),
    ('daily_cleanup', daily_cleanup, {'trigger': 'cron', 'hour': 2, 'minute': 0}),
]
