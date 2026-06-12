from functools import wraps

import redis


def single_executor(task_name: str, lock_ttl: int = 60):
    def decorator(func):
        @wraps(func)
        def wrapper():
            r = redis.Redis()
            lock_key = f'scheduler:lock:{task_name}'
            if r.set(lock_key, '1', nx=True, ex=lock_ttl):
                try:
                    func()
                finally:
                    r.delete(lock_key)
        return wrapper
    return decorator


@single_executor('cleanup_task', lock_ttl=120)
def cleanup_task():
    ...
