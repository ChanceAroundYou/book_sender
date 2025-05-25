from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.api import get_request_params
from app.database import Book, BookSeries, get_depend_db

router = APIRouter()


@router.get("/books", response_model=List[dict])
async def get_books_api(request: Request, db: Session = Depends(get_depend_db)):
    params = await get_request_params(request)
    params.setdefault("limit", 50)

    books = Book.query(db, **params)
    book_dicts = [book.to_dict() for book in books]
    return book_dicts


@router.get("/books/series", response_model=List[dict])
async def get_books_by_series_api(
    request: Request, db: Session = Depends(get_depend_db)
):
    """获取指定系列的所有图书"""
    params = await get_request_params(request)
    params.setdefault("limit", 50)
    series = params.pop("series", None)
    if not series:
        raise HTTPException(status_code=400, detail="Series is required")

    books = Book.query(db, series=series, **params)
    book_dicts = [book.to_dict() for book in books]
    return book_dicts


@router.get("/books/all", response_model=List[dict])
async def get_all_books_api(request: Request, db: Session = Depends(get_depend_db)):
    """获取所有图书，对每个系列取最新一本，OTHER系列显示全部"""
    params = await get_request_params(request)
    limit = int(params.pop("limit", 50))
    skip = int(params.pop("skip", 0))
    order_desc = params.pop("order_desc", True)
    order_by = params.pop("order_by", "date")
    # 获取所有系列
    series_list = BookSeries.get_series_list()
    result_book_dicts = []

    # 对每个系列获取最新一本
    for i, series in enumerate(series_list):
        if i < skip:
            continue
        if series != BookSeries.OTHER:
            book = Book.query(
                db, series=series, order_by="date", order_desc=True, first=True
            )
            if book:
                book_dict = book.to_dict()
                book_dict["title"] = series
                result_book_dicts.append(book_dict)

    books = Book.query(
        db,
        series=BookSeries.OTHER,
        order_by=order_by,
        order_desc=order_desc,
        skip=max(skip - len(result_book_dicts), 0),
        limit=limit - len(result_book_dicts),
    )
    result_book_dicts.extend([book.to_dict() for book in books])
    result_book_dicts.sort(key=lambda x: x[order_by], reverse=order_desc)
    return result_book_dicts


@router.get("/book", response_model=dict)
async def get_book_api(request: Request, db: Session = Depends(get_depend_db)):
    """获取单本图书详情"""
    params = await get_request_params(request)
    book = Book.query(db, first=True, **params)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.to_dict()


@router.post("/book", response_model=dict)
async def create_book_api(request: Request, db: Session = Depends(get_depend_db)):
    """创建新图书"""
    params = await get_request_params(request)
    book = Book.create(db, **params)
    return book.to_dict()


@router.put("/book", response_model=dict)
async def update_book_api(request: Request, db: Session = Depends(get_depend_db)):
    """更新图书信息"""
    params = await get_request_params(request)
    book_id = params.pop("id", None)
    if not book_id:
        raise HTTPException(status_code=400, detail="Book ID is required")

    book = Book.get_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.update(**params)
    return book.to_dict()


@router.delete("/book", response_model=dict)
async def delete_book_api(request: Request, db: Session = Depends(get_depend_db)):
    """删除图书"""
    params = await get_request_params(request)
    book = Book.query(db, first=True, **params)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.delete()
    return {"message": "Book deleted successfully"}


# @router.get("/books/s", response_model=List[str])
# async def get_categories_api(db: Session = Depends(get_depend_db)):
#     """获取所有图书分类"""
#     categories = BookSeries.get_series_list()
#     return categories
