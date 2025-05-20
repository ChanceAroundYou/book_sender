from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import Book, get_depend_db
from app.task.tasks import distribute_book_task, distribute_books_task

router = APIRouter()


@router.post("/distribute/books")
async def distribute_books_api(request: Request, db: Session = Depends(get_depend_db)):
    """批量发送书籍

    查询参数:
    - email: 收件人邮箱（可选）
    """
    try:
        params = dict(request.query_params)
        email = params.pop("email", "")
        if not email:
            return {"error": "未指定收件人邮箱"}

        params["file_size"] = 0
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
):
    """发送单本书籍"""
    try:
        params = dict(request.query_params)
        email = params.pop("email", "")
        if not email:
            return {"error": "未指定收件人邮箱"}

        distribute_book_task.delay(params, email)
        return {"message": f"发送书籍 {params.get('title', '')} 到 {email}"}
    except Exception as e:
        return {"error": str(e)}
