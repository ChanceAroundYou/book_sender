from celery import Celery

from app.config import settings

celery_app = Celery(
    "book_sender",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.task.tasks", "app.task.schedulers"],
)

# Celery 配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1小时超时
    worker_max_tasks_per_child=200,  # 每个worker处理200个任务后重启
    worker_prefetch_multiplier=settings.CELERY_WORKER_PREFETCH_MULTIPLIER,
    broker_connection_retry_on_startup=True,  # 修复警告
    worker_cancel_long_running_tasks_on_connection_loss=True,
    worker_concurrency=settings.CELERY_WORKER_CONCURRENCY,
)

celery_app.conf.beat_schedule = {
    "crawl_books": {
        "task": "app.task.schedulers.crawl_books_scheduler",
        "schedule": 60 * 60,
    },
    "crawl_book": {
        "task": "app.task.schedulers.crawl_book_scheduler",
        "schedule": 60 * 10,
    },
    "download_books": {
        "task": "app.task.schedulers.download_books_scheduler",
        "schedule": 60 * 10,
    },
    "distribute_books": {
        "task": "app.task.schedulers.distribute_books_scheduler",
        "schedule": 60 * 60,
    },
}
