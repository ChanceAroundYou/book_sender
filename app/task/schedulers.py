from loguru import logger

from app.celery_app import celery_app
from app.config import settings
from app.database import (Book, BookFormat, User, UserBook, UserBookStatus,
                          get_db)
from app.task.base import BaseTask
from app.task.tasks import crawl_books, download_book, send_books
from app.utils.compressor import compress_to_7z

max_retries = settings.CELERY_TASK_MAX_RETRIES
CATEGORIES = ["economist"]
DISTRIBUTE_TYPE = "ses"

@celery_app.task(
    bind=True, base=BaseTask,
    autoretry_for=(Exception,),  # 自动重试的异常类型
    retry_kwargs={'max_retries': max_retries},  # 最大重试次数
    retry_backoff=True,  # 使用指数退避
    retry_backoff_max=120,  # 最大重试间隔（秒）
    retry_jitter=True  # 添加随机抖动
)
def crawl_new_books(self, page=1):
    # 查询新书籍逻辑
    for category in CATEGORIES:
        logger.info(f"开始爬取{category}新书籍列表")
        crawl_books.delay(category, page=page)

@celery_app.task(
    bind=True, base=BaseTask,
    autoretry_for=(Exception,),  # 自动重试的异常类型
    retry_kwargs={'max_retries': max_retries},  # 最大重试次数
    retry_backoff=True,  # 使用指数退避
    retry_backoff_max=120,  # 最大重试间隔（秒）
    retry_jitter=True  # 添加随机抖动
)
def check_download(self):
    # 查询未下载书籍逻辑
    for category in CATEGORIES:
        with get_db() as db:
            books = Book.query(db, category=category, file_size=0, download_link={
                "operator": "!=",
                "value": ""
            })
            book_dicts = [book.to_dict() for book in books]
        
        logger.info(f"开始下载{category}书籍: {len(book_dicts)}本")
        for book_dict in book_dicts:
            logger.info(f"下载书籍: {book_dict['title']}")
            download_book.delay(category, book_dict)

@celery_app.task(
    bind=True, base=BaseTask,
    autoretry_for=(Exception,),  # 自动重试的异常类型
    retry_kwargs={'max_retries': max_retries},  # 最大重试次数
    retry_backoff=True,  # 使用指数退避
    retry_backoff_max=120,  # 最大重试间隔（秒）
    retry_jitter=True  # 添加随机抖动
)
def add_books_to_users(self):
    for category in CATEGORIES:
        with get_db() as db:
            users = User.query(db)
            for user in users:
                books = Book.query(db, category=category, id={
                    "operator": "not in",
                    "value": [ub.book_id for ub in UserBook.query(db, user_id=user.id)]
                })

                for book in books:
                    user_book = user.add_book(book)
                    if user_book:
                        logger.info(f"用户{user.id}添加书籍{book.title}完成")

@celery_app.task(
    bind=True, base=BaseTask,
    autoretry_for=(Exception,),  # 自动重试的异常类型
    retry_kwargs={'max_retries': max_retries},  # 最大重试次数
    retry_backoff=True,  # 使用指数退避
    retry_backoff_max=120,  # 最大重试间隔（秒）    
    retry_jitter=True  # 添加随机抖动
)
def distribute_books(self):
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
                send_books(DISTRIBUTE_TYPE, book_dicts, user_email)
            except Exception as e:
                logger.error(f"向{user_email}发送{category}书籍失败: {e}")
                continue

@celery_app.task(
    bind=True, base=BaseTask,
    autoretry_for=(Exception,),  # 自动重试的异常类型
    retry_kwargs={'max_retries': max_retries},  # 最大重试次t数
    retry_backoff=True,  # 使用指数退避
    retry_backoff_max=120,  # 最大重试间隔（秒
    retry_jitter=True  # 添加随机抖动
)
def compress_books(self):
    for category in CATEGORIES:
        with get_db() as db:
            books = Book.query(db, category=category, file_format=BookFormat.PDF)
            book_dicts = [book.to_dict() for book in books]

        for book_dict in book_dicts:
            compress_book(book_dict)

def compress_book(book_dict: dict):
    """压缩书籍任务"""
    file_path = book_dict.get("file_path", "")
    if not file_path:
        logger.warning("Book file path is empty.")
        return

    result = compress_to_7z(file_path)
    with get_db() as db:
        book = Book.query(db, download_link=book_dict.get("download_link"), first=True)
        if book:
            book.compressed(result['output_path'], result['compressed_size'])
            logger.info(f"Book {book.title} is compressed.")