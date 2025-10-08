from loguru import logger

from app.celery_app import celery_app
from app.config import settings
from app.database import Book, BookSeries, UserBookStatus, get_denpend_db, User, UserBook
from app.task.base import BaseTask
from app.task.tasks import (
    crawl_book_task,
    crawl_books_task,
    distribute_books_task,
    download_book_task,
)

max_retries = settings.CELERY_TASK_MAX_RETRIES
SERIES_LIST = BookSeries.get_series_list()


@celery_app.task(bind=True, base=BaseTask)
def crawl_books_scheduler(self: BaseTask, page=1):
    # 查询新书籍逻辑
    def _task():
        filtered_series_list = list(
            set(series for series in SERIES_LIST if series != BookSeries.OTHER)
        )

        logger.info(f"开始爬取书籍列表: {len(filtered_series_list)}个系列")
        for series in filtered_series_list:
            logger.info(f"开始爬取{series}新书籍列表")
            crawl_books_task.delay(series, page=page)

    return self.run_with_retry(_task)


@celery_app.task(bind=True, base=BaseTask)
def crawl_book_scheduler(self: BaseTask):
    # 查询新书籍逻辑
    def _task():
        with get_denpend_db() as db:
            book_dicts = []
            if books := (Book.query(db, download_link="", file_size=0) or []) + (
                Book.query(db, download_link=None, file_size=0) or []
            ):
                book_dicts = [book.to_dict() for book in books]

        logger.info(f"开始爬取书籍详情: {len(book_dicts)}本")
        for book_dict in book_dicts:
            logger.info(f"开始爬取{book_dict['title']}详情")
            crawl_book_task.delay(
                BookSeries.simplify_series(book_dict["series"]), book_dict
            )

    return self.run_with_retry(_task)


@celery_app.task(bind=True, base=BaseTask)
def download_books_scheduler(self: BaseTask):
    # 查询未下载书籍逻辑
    def _task():
        with get_denpend_db() as db:
            book_dicts = []
            if books := (Book.query(
                db, file_size=0, download_link={"operator": "is empty"}) or []
            ):
                book_dicts = [book.to_dict() for book in books]

        logger.info(f"开始下载书籍: {len(book_dicts)}本")
        for book_dict in book_dicts:
            logger.info(f"下载书籍: {book_dict['title']}")
            download_book_task.delay(book_dict)

    return self.run_with_retry(_task)


@celery_app.task(bind=True, base=BaseTask)
def distribute_books_scheduler(self: BaseTask):
    def _task():
        for series in SERIES_LIST:
            logger.info(f"开始分发{series}书籍")
            with get_denpend_db() as db:
                send_tasks = {}
                if books := Book.query(
                    db, series=series, file_size={"operator": ">", "value": 0}
                ):
                    for book in books:
                        for user_book in book.user_books:
                            if user_book.status == UserBookStatus.DOWNLOADED:
                                send_tasks.setdefault(user_book.user.email, []).append(
                                    book.to_dict()
                                )

            if not send_tasks:
                logger.info(f"没有{series}书籍需要分发")
                continue

            logger.info(f"开始分发{series}书籍")
            for user_email, book_dicts in send_tasks.items():
                if not book_dicts:
                    continue

                try:
                    logger.info(f"向{user_email}发送{series}书籍: {len(book_dicts)}本")
                    distribute_books_task(book_dicts, user_email)
                except Exception as e:
                    logger.error(f"向{user_email}发送{series}书籍失败: {e}")

    return self.run_with_retry(_task)

@celery_app.task(bind=True, base=BaseTask)
def check_user_books_scheduler(self: BaseTask):
    def _task():
        with get_denpend_db() as db:
            users = User.query(db)
            if not users:
                return

            for user in users:
                user.check_subscriptions()

    return self.run_with_retry(_task)
