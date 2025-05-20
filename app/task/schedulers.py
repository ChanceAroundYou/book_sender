from loguru import logger

from app.celery_app import celery_app
from app.config import settings
from app.database import Book, BookCategory, UserBookStatus, get_db
from app.task.base import BaseTask
from app.task.tasks import (crawl_books_task, distribute_books_task,
                            download_book_task)

max_retries = settings.CELERY_TASK_MAX_RETRIES
CATEGORIES = BookCategory.get_categories()

@celery_app.task(bind=True, base=BaseTask)
def crawl_books_scheduler(self: BaseTask, page=1):
    # 查询新书籍逻辑
    def _task():
        for category in CATEGORIES:
            if category == BookCategory.OTHER or '_' in category:
                continue

            logger.info(f"开始爬取{category}新书籍列表")
            crawl_books_task.delay(category, page=page)

    return self.run_with_retry(_task)

@celery_app.task(bind=True, base=BaseTask)
def download_books_scheduler(self: BaseTask):
    # 查询未下载书籍逻辑
    def _task():
        with get_db() as db:
            books = Book.query(db, file_size=0, download_link={
                "operator": "!=",
                "value": ""
            })
            book_dicts = [book.to_dict() for book in books]
        
        logger.info(f"开始下载书籍: {len(book_dicts)}本")
        for book_dict in book_dicts:
            logger.info(f"下载书籍: {book_dict['title']}")
            download_book_task.delay(book_dict)

    return self.run_with_retry(_task)

@celery_app.task(bind=True, base=BaseTask)
def distribute_books_scheduler(self: BaseTask):
    def _task():
        for category in CATEGORIES:
            send_tasks = {}
            with get_db() as db:
                books = Book.query(db, category=category, file_size={'operator': '>', 'value': 0})
                for book in books:
                    for user_book in book.user_books:
                        if user_book.status == UserBookStatus.DOWNLOADED:
                            send_tasks.setdefault(user_book.user.email, []).append(book.to_dict())

            if not send_tasks:
                logger.info(f"没有{category}书籍需要分发")
                continue

            logger.info(f"开始分发{category}书籍")
            for user_email, book_dicts in send_tasks.items():
                if not book_dicts:
                    continue

                try:
                    logger.info(f"向{user_email}发送{category}书籍: {len(book_dicts)}本")
                    distribute_books_task(book_dicts, user_email)
                except Exception as e:
                    logger.error(f"向{user_email}发送{category}书籍失败: {e}")
                    continue

    return self.run_with_retry(_task)
