import uuid


def new_trace_id(job_id: str) -> str:
    # 任务名 + 8 位随机 hex，每次执行唯一且日志里一眼可读
    return f'{job_id}-{uuid.uuid4().hex[:8]}'
