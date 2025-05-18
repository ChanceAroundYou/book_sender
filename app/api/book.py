from typing import List

from fastapi import APIRouter, HTTPException, Request

from app.database import get_db, Book

router = APIRouter()


@router.get("/books", response_model=List[dict])
async def get_books(request: Request):
    params = dict(request.query_params)
    params.setdefault('limit', 50)

    with get_db() as db:
        books = Book.query(db, **params)
        book_dicts = [book.to_dict() for book in books]
        return book_dicts


@router.get("/books/{book_id}", response_model=dict)
async def get_book(book_id: int):
    """获取单本图书详情"""
    with get_db() as db:
        book = Book.get_by_id(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book.to_dict()


@router.post("/books", response_model=dict)
async def create_book(request: Request):
    """创建新图书"""
    params = dict(request.query_params)

    with get_db() as db:
        book = Book.create(db, **params)
        return book.to_dict()


@router.put("/books/{book_id}", response_model=dict)
async def update_book(request: Request, book_id: int):
    """更新图书信息"""
    params = dict(request.query_params)

    with get_db() as db:
        book = Book.get_by_id(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        book.update(**params)
        return book.to_dict()


@router.delete("/books/{book_id}")
async def delete_book(book_id: int):
    """删除图书"""
    with get_db() as db:
        book = Book.get_by_id(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        book.delete()
        return {"message": "Book deleted successfully"}
