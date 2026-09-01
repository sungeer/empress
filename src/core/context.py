import uuid


def new_trace_id() -> str:
    trace_id = uuid.uuid4().hex[:16]  # 'd8961c3c4f884505'
    return trace_id
