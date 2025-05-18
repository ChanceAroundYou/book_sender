from typing import List

from fastapi import APIRouter, HTTPException, Request
from loguru import logger

from app.database import get_db, User

router = APIRouter()


@router.get("/users", response_model=List[dict])
async def get_users(request: Request):
    """获取用户列表"""
    params = dict(request.query_params)
    params.setdefault('limit', 50)
    
    with get_db() as db:
        users = User.query(db, **params)
        return [user.to_dict() for user in users]
    

@router.get("/users/{user_id}", response_model=dict)
async def get_user(user_id: int):
    """获取用户详情"""
    with get_db() as db:
        user = User.get_by_id(db, user_id)
        if user:
            return user.to_dict()
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/users", response_model=dict)
async def create_user(request: Request):
    """创建用户"""
    params = dict(request.query_params)

    with get_db() as db:
        user = User.create(db, **params)
        return user.to_dict()


@router.put("/users/{user_id}", response_model=dict)
async def update_user(request: Request, user_id: int):
    """更新用户"""
    params = dict(request.query_params)

    with get_db() as db:
        user = User.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.update(**params)
        return user.to_dict()



@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    """删除用户"""
    with get_db() as db:
        user = User.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.delete()
        return {"message": "User deleted successfully"}


@router.put("/users/{user_id}/subscriptions")
async def add_user_subscription(request: Request, user_id: int):
    """添加用户订阅"""
    params = dict(request.query_params)
    category = params.get("category", "")
    date = params.get("date", "")

    if not category:
        raise HTTPException(status_code=400, detail="Category is required")

    with get_db() as db:
        user = User.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.add_subscription(category, date)
        return user.to_dict()

@router.delete("/users/{user_id}/subscriptions")
async def remove_user_subscription(request: Request, user_id: int):
    """删除用户订阅"""
    params = dict(request.query_params)
    category = params.get("category", "")

    if not category:
        raise HTTPException(status_code=400, detail="Category is required")

    with get_db() as db:
        user = User.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.remove_subscription(category)
        return user.to_dict()

