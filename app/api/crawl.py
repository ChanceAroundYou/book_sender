from fastapi import APIRouter
from loguru import logger

from app.task.tasks import crawl_book, crawl_books

router = APIRouter()

@router.post("/crawl/book_list/{category}")
async def crawl_book_list(
    page: int = 1,
    category: str = "economist",
):
    try:
        logger.info(f'Starting to crawl book list page: {page}.')
        crawl_books.delay(category, page)
        return {"message": "Book list crawl task start."}
    except Exception as e:
        return {"error": str(e)}


@router.post("/crawl/book/{category}")
async def crawl_book(
    book_dict: dict,
    category: str = "economist",
):
    try:
        logger.info(
            f"Starting to crawl book {book_dict.get('title', '')}, detail link: {book_dict.get('detail_link', '')}."
        )
        crawl_book.delay(category, book_dict)
        return {"message": "Book crawl task start."}
    except Exception as e:
        return {"error": str(e)}
