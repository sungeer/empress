from redis import Redis, Retry


r = Redis(
    host='localhost',
    port=6379,
    # 定期检测连接健康，发现坏连接就丢弃重建
    health_check_interval=30,
    retry_on_timeout=True,
)
