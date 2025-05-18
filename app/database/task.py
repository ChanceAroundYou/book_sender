from datetime import UTC, datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Session, relationship

from app.database.base import BaseModel, ModelMixin
from app.utils.convert_mixin import to_dict, to_iterable


class TaskStatus:
    PENDING = "pending"
    STARTED = "started"
    SUCCESS = "success"
    FAILURE = "failure"
    RETRY = "retry"


class Task(BaseModel, ModelMixin['Task']):
    __tablename__ = "tasks"

    id = Column(String(100), primary_key=True, index=True)
    name = Column(String(100))
    status = Column(String(20), default=TaskStatus.PENDING)
    args = Column(JSON)  # 任务参数
    kwargs = Column(JSON)
    result = Column(JSON)  # 任务结果
    error = Column(Text)  # 错误信息
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    # 关联的任务
    parent_id = Column(String(100), ForeignKey("tasks.id"), nullable=True)
    parent = relationship("Task", remote_side=[id], backref="child_tasks")

    def __init__(self, **kwargs):
        if 'id' not in kwargs:
            raise ValueError("Task ID must be provided")
        super().__init__(**kwargs)

    @classmethod
    def create(cls, db: Session, ignore_id: bool=False, **kwargs) -> 'Task':
        return super().create(db, ignore_id, **kwargs)

    def start(self, args=None, kwargs=None):
        self.update(
            status=TaskStatus.STARTED,
            started_at=datetime.now(UTC),
            args=to_iterable(args),
            kwargs=to_dict(kwargs)
        )

    def complete(self, result=None):
        self.update(
            status=TaskStatus.SUCCESS,
            completed_at=datetime.now(UTC),
            result=to_dict(result)
        )

    def fail(self, error):
        self.update(
            status=TaskStatus.FAILURE,
            completed_at=datetime.now(UTC),
            error=f'type: {str(type(error))}, message: {str(error)}'
        )

    def retry(self):
        self.update(
            status=TaskStatus.RETRY,
            completed_at=datetime.now(UTC)
        )
