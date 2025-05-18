import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, Request

from app.database import get_db, Book
from app.task.tasks import download_book
from loguru import logger

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=10)


async def download_books_background_task(book_category: str, params: dict):
    try:
        with get_db() as db:
            params["file_size"] = 0
            params["download_link"] = {"operator": "!=", "value": ""}
            books = Book.query(db, **params)
            book_dicts = [book.to_dict() for book in books]
        
        for book_dict in book_dicts:
            download_book.delay(book_category, book_dict)
        logger.info(f"Book list with {len(book_dicts)} books starts to download.")
    except Exception as e:
        raise Exception(f"Error in background task: {str(e)}")

@router.post("/download/book_list/{category}")
async def download_books(
    request: Request,
    category: str = "economist",
):
    """创建下载任务"""
    try:
        params = dict(request.query_params)
        params.pop('category', None)
        asyncio.create_task(
            download_books_background_task(category, params)
        )
        return {"message": "Book list download task start."}
    except Exception as e:
        return {"error": str(e)}


@router.post("/download/book/{category}")
async def download_book(
    book_dict: dict,
    category: str = "economist",
):
    """创建下载任务"""
    try:
        book_title = book_dict.get('title', '')
        download_link = book_dict.get('download_link', '')
        logger.info(f"Starting to download book {book_title}, download link: {download_link}.")
        download_book.delay(category, book_dict)
        return {"message": f"Book {book_title} download task start."}
    except Exception as e:
        return {"error": str(e)}
