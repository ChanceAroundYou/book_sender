import asyncio
from functools import wraps
from typing import Any, Dict

from celery import Task as CeleryTask
from loguru import logger

from app.config import settings
from app.database import Task, get_denpend_db


class BaseTask(CeleryTask):
    def before_start(self, task_id, args, kwargs):
        with get_denpend_db() as db:
            task = Task.get_by_id(db, task_id)
            if not task:
                task = Task.create(db, id=task_id, name=self.name)
            task.start(args, kwargs)

    def on_success(self, retval: Any, task_id: str, args: tuple, kwargs: Dict) -> None:
        """任务成功时的回调"""
        with get_denpend_db() as db:
            task = Task.get_by_id(db, task_id)
            if task:
                task.complete(retval)

    def on_failure(
        self, exc: Exception, task_id: str, args: tuple, kwargs: Dict, einfo: Any
    ) -> None:
        """任务失败时的回调"""
        with get_denpend_db() as db:
            task = Task.get_by_id(db, task_id)
            if task:
                task.fail(exc)

    def on_retry(
        self, exc: Exception, task_id: str, args: tuple, kwargs: Dict, einfo: Any
    ) -> None:
        """任务重试时的回调"""
        with get_denpend_db() as db:
            task = Task.get_by_id(db, task_id)
            if task:
                task.retry()

    def run_with_retry(self, func, *args, **kwargs):
        """同步运行任务，并重试"""
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"任务失败，{e}")
            retries = self.request.retries
            max_retries = settings.CELERY_TASK_MAX_RETRIES
            countdown = 10 * (2**retries)
            if retries < max_retries:
                logger.warning(f"重试 (attempt {retries + 1}/{max_retries})")
                raise self.retry(exc=e, countdown=countdown, max_retries=max_retries)
            else:
                logger.error(f"重试失败，已重试{max_retries}次: {str(e)}")
                raise e

    @staticmethod
    def retry_decorator(is_async: bool = False):
        """装饰器：将带有 self 参数的任务函数包装为通过 self.run_with_retry 调用。

        用法示例：
        @celery_app.task(bind=True, base=BaseTask)
        @BaseTask.retry_decorator(is_async=False)
        def crawl_books_scheduler(...):
            ...
        """
        def func_wrapper(func):
            
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if is_async:
                    return self.run_with_retry(lambda: asyncio.run(func(*args, **kwargs)))
                return self.run_with_retry(func, *args, **kwargs)

            return wrapper
        return func_wrapper
