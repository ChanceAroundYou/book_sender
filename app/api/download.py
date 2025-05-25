from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.api import get_request_params
from app.database import Book, get_depend_db
from app.task.tasks import download_book_task

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=10)


@router.post("/download/books")
async def download_books_api(request: Request, db: Session = Depends(get_depend_db)):
    """创建下载任务"""
    try:
        params = dict(request.query_params)
        params["file_size"] = 0
        params["download_link"] = {"operator": "!=", "value": ""}
        books = Book.query(db, **params)
        book_dicts = [book.to_dict() for book in books]

        for book_dict in book_dicts:
            download_book_task.delay(book_dict)
        return {"message": f"{len(book_dicts)} books starts to download."}
    except Exception as e:
        return {"error": str(e)}


@router.post("/download/book")
async def download_book_api(
    request: Request,
    db: Session = Depends(get_depend_db),
):
    """创建下载任务"""
    try:
        params = await get_request_params(request)
        book = Book.query(db, first=True, **params)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        download_book_task.delay(book.to_dict())
        return {"message": f"Book {book.title} download task start."}
    except Exception as e:
        return {"error": str(e)}
