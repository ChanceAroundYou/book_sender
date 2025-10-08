import asyncio

from loguru import logger

from app.celery_app import celery_app
from app.config import settings
from app.crawler import create_crawler
from app.database import Book, BookSeries, get_denpend_db
from app.distributor import create_distributor
from app.downloader import create_downloader
from app.task.base import BaseTask


@celery_app.task(bind=True, base=BaseTask)
def crawl_books_task(self: BaseTask, series: str, page: int = 1):
    """爬取书籍列表任务"""

    async def _task():
        async with create_crawler(BookSeries.simplify_series(series)) as crawler:
            book_dicts = await crawler.get_books(page)

        if not book_dicts:
            logger.warning("No books found.")
            return

        logger.info(f"Book list is crawled, got {len(book_dicts)} books.")

        for book_dict in book_dicts:
            detail_link = book_dict.get("detail_link", "")
            if not detail_link:
                continue

            with get_denpend_db() as db:
                book_db = Book.query(db, detail_link=detail_link, first=True)
                if not book_db:
                    book_db = Book.create(db, **book_dict)
                    logger.info(f"Book {book_db.title} added to the database.")

            crawl_book_task.delay(series, book_dict)

        logger.info(f"Book list page {page} is crawled.")

    return self.async_run_with_retry(_task)


@celery_app.task(bind=True, base=BaseTask)
def crawl_book_task(self: BaseTask, series: str, book_dict: dict):
    """爬取书籍详情任务"""

    async def _task(book_dict):
        detail_link = book_dict.get("detail_link", "")
        if detail_link == "":
            logger.warning("Book detail link is empty.")
            return

        with get_denpend_db() as db:
            book = Book.query(db, detail_link=detail_link, first=True)
            if not book:
                logger.warning("Book not found in the database.")
                return
            elif book.download_link:
                logger.info(f"Download link is {book.download_link}")
                logger.info(f"Book {book.title} detail is already crawled.")
                return
            book_dict = book.to_dict()

        async with create_crawler(BookSeries.simplify_series(series)) as crawler:
            book_dict = await crawler.get_book(book_dict)
            if not book_dict.get("download_link"):
                logger.warning("Book detail is not found.")
                return

        with get_denpend_db() as db:
            book = Book.query(db, detail_link=detail_link, first=True)
            if book:
                book.update(**book_dict)
                logger.info(f"Book {book.title} detail is crawled.")

    return self.async_run_with_retry(_task, book_dict)


@celery_app.task(bind=True, base=BaseTask)
def download_book_task(self: BaseTask, book_dict: dict):
    """下载书籍任务"""

    async def _task(book_dict):
        download_link = book_dict.get("download_link", "")
        if not download_link:
            logger.warning("Book download link is empty.")
            return

        with get_denpend_db() as db:
            book = Book.query(db, download_link=download_link, first=True)
            if not book:
                logger.warning("Book not found in the database.")
                return
            elif not book.file_path and book.file_size > 0:
                logger.info(f"Book {book.title} is already downloaded.")
                return
            book_dict = book.to_dict()

        downloader = create_downloader(settings.DOWNLOADER_TYPE)
        book_dict = await downloader.download_book(book_dict)
        file_size = book_dict.get("file_size", 0)
        file_path = book_dict.get("file_path", "")
        file_format = book_dict.get("file_format", "")

        if file_size == 0 or file_path == "" or file_format == "":
            raise Exception("下载失败")

        with get_denpend_db() as db:
            book = Book.query(db, first=True, download_link=download_link)
            if book:
                book.downloaded(file_path, file_size, file_format)
                logger.info(f"Book {book.title} is downloaded.")

    return self.async_run_with_retry(_task, book_dict)


@celery_app.task(bind=True, base=BaseTask)
def distribute_book_task(self: BaseTask, book_dict: dict, email: str = ''):
    """分发书籍任务"""

    async def _task(book_dict):
        try:
            distributor = create_distributor(settings.DISTRIBUTOR_TYPE)

            if book_dict.get("file_size", 0) == 0:
                logger.warning(f"书籍 {book_dict.get('title')} 未下载")
                return

            # 分发书籍
            success = await distributor.send_book(book_dict, email)
            if not success:
                raise Exception("分发失败")

            with get_denpend_db() as db:
                book = Book.query(
                    db, download_link=book_dict["download_link"], first=True
                )
                if book:
                    book.distributed(email=email)
                    logger.info(f"Successfully distributed book: {book_dict['title']}")

        except Exception as e:
            logger.error(f"分发失败: {str(e)}")
            raise e

    return asyncio.run(_task(book_dict))


@celery_app.task(bind=True, base=BaseTask)
def distribute_books_task(self: BaseTask, book_dicts: list[dict], email: str = ''):
    """批量分发书籍任务"""

    async def _task(book_dicts):
        try:
            distributor = create_distributor(settings.DISTRIBUTOR_TYPE)

            book_dicts = [
                book_dict
                for book_dict in book_dicts
                if book_dict.get("file_size", 0) > 0
            ]

            if not book_dicts:
                logger.warning("没有书籍需要分发")
                return

            success = await distributor.send_books(book_dicts, email)
            if not success:
                raise Exception("分发失败")

            with get_denpend_db() as db:
                for book_dict in book_dicts:
                    book = Book.query(
                        db, download_link=book_dict["download_link"], first=True
                    )
                    if book:
                        book.distributed(email=email)

            logger.info(f"成功分发书籍: {len(book_dicts)}本")

        except Exception as e:
            logger.error(f"分发失败: {str(e)}")
            raise e

    return asyncio.run(_task(book_dicts))
