from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import User, get_depend_db

router = APIRouter()


@router.get("/users", response_model=List[dict])
async def get_users_api(request: Request, db: Session = Depends(get_depend_db)):
    """获取用户列表"""
    params = dict(request.query_params)
    params.setdefault("limit", 50)

    users = User.query(db, **params)
    return [user.to_dict() for user in users]


@router.get("/users/{user_id}", response_model=dict)
async def get_user_api(user_id: int, db: Session = Depends(get_depend_db)):
    """获取用户详情"""
    user = User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_dict()


@router.post("/users", response_model=dict)
async def create_user_api(request: Request, db: Session = Depends(get_depend_db)):
    """创建用户"""
    params = dict(request.query_params)
    user = User.create(db, **params)
    return user.to_dict()


@router.put("/users/{user_id}", response_model=dict)
async def update_user_api(
    request: Request, user_id: int, db: Session = Depends(get_depend_db)
):
    """更新用户"""
    params = dict(request.query_params)
    user = User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.update(**params)
    return user.to_dict()


@router.delete("/users/{user_id}", response_model=dict)
async def delete_user_api(user_id: int, db: Session = Depends(get_depend_db)):
    """删除用户"""
    user = User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete()
    return {"message": "User deleted successfully"}


@router.put("/users/{user_id}/subscriptions")
async def add_user_subscription_api(
    request: Request, user_id: int, db: Session = Depends(get_depend_db)
):
    """添加用户订阅"""
    params = dict(request.query_params)
    category = params.get("category", "")
    date = params.get("date", "")

    if not category:
        raise HTTPException(status_code=400, detail="Category is required")

    user = User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.add_subscription(category, date)
    return user.to_dict()


@router.delete("/users/{user_id}/subscriptions")
async def remove_user_subscription_api(
    request: Request, user_id: int, db: Session = Depends(get_depend_db)
):
    """删除用户订阅"""
    params = dict(request.query_params)
    category = params.get("category", "")

    if not category:
        raise HTTPException(status_code=400, detail="Category is required")

    user = User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.remove_subscription(category)
    return user.to_dict()
