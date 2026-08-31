# 冒烟测试：trace_id 生成 + 任务执行时的日志绑定
# 运行：.venv\Scripts\python.exe tests/trace_test.py
import sys
from io import StringIO
from pathlib import Path

# 把项目根目录加进 sys.path，保证 `import src` 可用
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from loguru import logger

from src.core.context import new_trace_id
from src.core.logger import _inject_trace_id
from src.core.scheduler import _with_trace


def test_new_trace_id_format_and_unique():
    a = new_trace_id('daily_cleanup')
    b = new_trace_id('daily_cleanup')
    # 格式：任务名前缀 + '-' + 8 位 hex
    assert a.startswith('daily_cleanup-')
    assert len(a.split('-', 1)[1]) == 8
    # 每次执行 ID 必须不同
    assert a != b


def test_with_trace_binds_trace_id_inside_and_default_outside():
    logger.remove()
    logger.configure(patcher=_inject_trace_id)
    captured = StringIO()
    logger.add(captured, format='{extra[trace_id]} {message}', level='INFO', colorize=False)

    def task():
        logger.info('inside')
        return 'ok'

    assert _with_trace('task_a', task)() == 'ok'
    logger.info('outside')

    lines = captured.getvalue().strip().splitlines()
    # 任务作用域内的日志带 trace_id（任务名前缀）
    assert lines[0].startswith('task_a-') and lines[0].endswith('inside')
    # 作用域外的日志回落到默认 '-'
    assert lines[1] == '- outside'


if __name__ == '__main__':
    test_new_trace_id_format_and_unique()
    test_with_trace_binds_trace_id_inside_and_default_outside()
    print('trace test passed')
