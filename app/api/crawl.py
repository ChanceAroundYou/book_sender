from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session

from app.api import get_request_params
from app.task.tasks import crawl_book_task, crawl_books_task
from app.database import Book, get_depend_db

router = APIRouter()


@router.post("/crawl/books/{series}")
async def crawl_books_api(
    request: Request,
    series: str = "economist",
):
    try:
        params = await get_request_params(request)
        page = int(params.pop("page", 1))
        crawl_books_task.delay(series, page)
        return {"message": "Book list crawl task start."}
    except Exception as e:
        return {"error": str(e)}


@router.post("/crawl/book/{series}")
async def crawl_book_api(
    request: Request,
    series: str = "economist",
    db: Session = Depends(get_depend_db),
):
    try:
        params = await get_request_params(request)
        params.pop("series", None)
        if not (book := Book.query_first(db, **params)):
            raise HTTPException(status_code=404, detail="Book not found")
        crawl_book_task.delay(series, book.to_dict())
        return {"message": "Book crawl task start."}
    except Exception as e:
        return {"error": str(e)}
