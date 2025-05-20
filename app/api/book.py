from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import Book, get_depend_db

router = APIRouter()


@router.get("/books", response_model=List[dict])
async def get_books_api(request: Request, db: Session = Depends(get_depend_db)):
    params = dict(request.query_params)
    params.setdefault("limit", 50)

    books = Book.query(db, **params)
    book_dicts = [book.to_dict() for book in books]
    return book_dicts


@router.get("/books/{book_id}", response_model=dict)
async def get_book_api(book_id: int, db: Session = Depends(get_depend_db)):
    """获取单本图书详情"""
    book = Book.get_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.to_dict()


@router.post("/books", response_model=dict)
async def create_book_api(request: Request, db: Session = Depends(get_depend_db)):
    """创建新图书"""
    params = dict(request.query_params)
    book = Book.create(db, **params)
    return book.to_dict()


@router.put("/books/{book_id}", response_model=dict)
async def update_book_api(
    request: Request, book_id: int, db: Session = Depends(get_depend_db)
):
    """更新图书信息"""
    params = dict(request.query_params)
    book = Book.get_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.update(**params)
    return book.to_dict()


@router.delete("/books/{book_id}")
async def delete_book_api(book_id: int, db: Session = Depends(get_depend_db)):
    """删除图书"""
    book = Book.get_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.delete()
    return {"message": "Book deleted successfully"}
