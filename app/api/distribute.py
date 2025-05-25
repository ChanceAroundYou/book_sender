from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.database import Book, get_depend_db, UserBook, UserBookStatus
from app.task.tasks import distribute_book_task, distribute_books_task
from app.api import get_request_params

router = APIRouter()


@router.post("/distribute/books")
async def distribute_books_api(request: Request, db: Session = Depends(get_depend_db)):
    """批量发送书籍

    查询参数:
    - email: 收件人邮箱（可选）
    """
    try:
        params = await get_request_params(request)
        email = params.pop("email", "")
        if not email:
            return {"error": "未指定收件人邮箱"}

        params["file_size"] = {"operator": ">", "value": 0}
        params["download_link"] = {"operator": "!=", "value": ""}
        
        books = Book.query(db, **params)
        book_dicts = [book.to_dict() for book in books]

        distribute_books_task.delay(book_dicts, email)
        return {"message": f"发送{len(books)}本书籍到 {email}"}
    except Exception as e:
        return {"error": str(e)}


@router.post("/distribute/book")
async def distribute_book_api(
    request: Request,
    db: Session = Depends(get_depend_db),
):
    """发送单本书籍"""
    try:
        params = await get_request_params(request)
        email = params.pop("email", "")
        if not email:
            return {"error": "未指定收件人邮箱"}

        book = Book.query(db, first=True, **params)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        distribute_book_task.delay(book.to_dict(), email)
        return {"message": f"发送书籍 {book.title} 到 {email}"}
    except Exception as e:
        return {"error": str(e)}

@router.post("/distribute/series")
async def distribute_series_api(request: Request, db: Session = Depends(get_depend_db)):
    """批量发送书籍

    查询参数:
    - email: 收件人邮箱（可选）
    - series: 系列名称
    """
    try:
        params = await get_request_params(request)
        email = params.pop("email", "")
        if not email:
            return {"error": "未指定收件人邮箱"}

        series = params.pop("series", "")
        if not series:
            return {"error": "未指定系列"}

        params["file_size"] = {"operator": ">", "value": 0}
        params["download_link"] = {"operator": "!=", "value": ""}
        
        books = db.query(Book).filter(
            (Book.series == series) &
            (Book.file_size > 0) &
            (Book.download_link != "")
        ).join(UserBook).filter(UserBook.status == UserBookStatus.DOWNLOADED).all()
        book_dicts = [book.to_dict() for book in books]

        distribute_books_task.delay(book_dicts, email)
        return {"message": f"发送{len(books)}本书籍到 {email}"}
    except Exception as e:
        return {"error": str(e)}