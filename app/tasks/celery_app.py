"""
Celery 应用配置
"""
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

# 创建 Celery 应用
celery_app = Celery(
    "alpha_arena",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.strategy_runner",
        "app.tasks.price_updater",
        "app.tasks.season_monitor",
    ]
)

# Celery 配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 分钟超时
    broker_connection_retry_on_startup=True,  # 启动时重试连接
)

# Celery Beat 调度配置
celery_app.conf.beat_schedule = {
    # 每 5 分钟执行策略
    "run-strategies": {
        "task": "app.tasks.strategy_runner.run_all_strategies",
        "schedule": crontab(minute="*/5"),
    },
    # 每分钟监控赛季状态
    "monitor-seasons": {
        "task": "app.tasks.season_monitor.check_season_status",
        "schedule": crontab(minute="*"),
    },
    # 每 30 秒更新价格
    "update-prices": {
        "task": "app.tasks.price_updater.update_crypto_prices",
        "schedule": 30.0,
    },
    # 每分钟更新持仓价格
    "update-positions": {
        "task": "app.tasks.price_updater.update_positions_prices",
        "schedule": crontab(minute="*"),
    },
    # 每 5 分钟记录价值历史
    "record-value-history": {
        "task": "app.tasks.strategy_runner.record_value_history",
        "schedule": crontab(minute="*/5"),
    },
}

if __name__ == "__main__":
    celery_app.start()

