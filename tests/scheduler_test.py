# 冒烟测试：任务注册表 + 调度器构建
# 运行：.venv\Scripts\python.exe tests/scheduler_test.py
import sys
from pathlib import Path

# 把项目根目录加进 sys.path，保证 `import src` 可用
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from apscheduler.schedulers.blocking import BlockingScheduler

from src import tasks
from src.core.scheduler import build_scheduler


def test_all_tasks_callable():
    # JOBS 里的每个任务都必须是可调用的模块级函数（APScheduler 要求全局可 import）
    for job_id, func, _kwargs in tasks.JOBS:
        assert callable(func), job_id


def test_build_scheduler():
    sched = build_scheduler()
    assert isinstance(sched, BlockingScheduler)


def test_register_all_jobs():
    # 注册表里的每个任务都能通过 add_job 成功注册（校验 trigger 参数拼写）
    sched = build_scheduler()
    for job_id, func, kwargs in tasks.JOBS:
        sched.add_job(func, id=job_id, replace_existing=True, **kwargs)
    assert len(sched.get_jobs()) == len(tasks.JOBS)


if __name__ == '__main__':
    test_all_tasks_callable()
    test_build_scheduler()
    test_register_all_jobs()
    print('scheduler test passed')
