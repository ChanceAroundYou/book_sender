from typing import List

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import func

from app.database import get_db, Task

router = APIRouter()


@router.get("/tasks", response_model=List[dict])
async def get_tasks(
    request: Request,
):
    """获取任务列表，支持多种搜索条件
    
    参数:
    - skip: 跳过记录数
    - limit: 返回记录数
    """
    with get_db() as db:
        # 处理查询参数
        params = dict(request.query_params)
        params.setdefault("order_by", "created_at")

        tasks = Task.query(db, **params)
        task_dicts = [task.to_dict() for task in tasks]
        return task_dicts


@router.get("/tasks/{task_id}", response_model=dict)
async def get_task(task_id: str):
    """获取单个任务详情"""
    with get_db() as db:
        task = Task.get_by_id(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task.to_dict()


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """删除任务"""
    with get_db() as db:
        task = Task.get_by_id(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    
        task.delete()
        return {"message": "Task deleted successfully"}

@router.get("/tasks/status/summary")
async def get_task_status_summary():
    """获取任务状态统计
    
    参数:
    - task_type: 可选的任务类型过滤
    """
    with get_db() as db:
        query = db.query(
            Task.status,
            func.count(Task.id).label('count')
        )

        summary = query.group_by(Task.status).all()
        return {
            status: count for status, count in summary
        }
