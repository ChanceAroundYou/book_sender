from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import Task, get_depend_db

router = APIRouter()


@router.get("/tasks", response_model=List[dict])
async def get_tasks_api(request: Request, db: Session = Depends(get_depend_db)):
    """获取任务列表，支持多种搜索条件

    参数:
    - skip: 跳过记录数
    - limit: 返回记录数
    """
    params = dict(request.query_params)
    params.setdefault("order_by", "created_at")
    params.setdefault("limit", 50)

    tasks = Task.query(db, **params)
    task_dicts = [task.to_dict() for task in tasks]
    return task_dicts


@router.get("/tasks/{task_id}", response_model=dict)
async def get_task_api(task_id: str, db: Session = Depends(get_depend_db)):
    """获取单个任务详情"""
    task = Task.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.to_dict()


@router.delete("/tasks/{task_id}")
async def delete_task_api(task_id: str, db: Session = Depends(get_depend_db)):
    """删除任务"""
    task = Task.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.delete()
    return {"message": "Task deleted successfully"}


@router.get("/tasks/status/summary")
async def get_task_status_summary_api(db: Session = Depends(get_depend_db)):
    """获取任务状态统计

    参数:
    - task_type: 可选的任务类型过滤
    """
    query = db.query(Task.status, func.count(Task.id).label("count"))

    summary = query.group_by(Task.status).all()
    return {status: count for status, count in summary}
