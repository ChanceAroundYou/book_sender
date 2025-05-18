import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

from fastapi import APIRouter, Request
from loguru import logger

from app.database import get_db, Book
from app.task.tasks import send_book

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=10)


async def distribute_books_background_task(task_type: str="ses", params: Dict={}, email: str = None):
    """批量发送书籍的后台任务"""
    try:
        with get_db() as db:
            params["file_size"] = 0
            params["download_link"] = {"operator": "!=", "value": ""}

            books = Book.query(db, **params)
            book_dicts = [book.to_dict() for book in books]

            # 使用默认收件人或指定收件人
            if not email:
                logger.error("未指定收件人邮箱")
                return

        for book_dict in book_dicts:
            if not (book_dict.get("file_path") and book_dict.get("file_size") > 0):
                logger.warning(f"书籍 {book_dict.get('title')} 未下载")
                continue

            send_book.delay(task_type, book_dict, email)
        
        logger.info(f"发送{len(books)}本书籍到 {email}")
            
    except Exception as e:
        raise Exception(f"后台任务错误: {str(e)}")

@router.post("/distribute/book_list/{task_type}")
async def distribute_books(
    request: Request,
    email: str = '',
    task_type: str = "ses"
):
    """批量发送书籍
    
    查询参数:
    - email: 收件人邮箱（可选）
    """
    try:
        params = dict(request.query_params)
        params.pop("email", '')
        asyncio.create_task(
            distribute_books_background_task(task_type, params, email)
        )

        return {"message": f"开始发送书籍到 {email}"}
    except Exception as e:
        return {"error": str(e)}


@router.post("/distribute/book/{task_type}")
async def distribute_book(
    request: Request,
    email: str = '',
    task_type: str = "ses"
):
    """发送单本书籍"""
    try:
        params = dict(request.query_params)
        params.pop("email", '')
        logger.info(f"发送书籍 {params.get('title', '')} 到 {email}")
        send_book.delay(task_type, params, email)
        return {"message": f"开始发送书籍 {params.get('title', '')} 到 {email}"}
    except Exception as e:
        return {"error": str(e)}
