from fastapi import APIRouter

from app.task.tasks import crawl_book_task, crawl_books_task

router = APIRouter()

@router.post("/crawl/books/{category}")
async def crawl_books_api(
    page: int = 1,
    category: str = "economist",
):
    try:
        crawl_books_task.delay(category, page)
        return {"message": "Book list crawl task start."}
    except Exception as e:
        return {"error": str(e)}


@router.post("/crawl/book/{category}")
async def crawl_book_api(
    book_dict: dict,
    category: str = "economist",
):
    try:
        crawl_book_task.delay(category, book_dict)
        return {"message": "Book crawl task start."}
    except Exception as e:
        return {"error": str(e)}
