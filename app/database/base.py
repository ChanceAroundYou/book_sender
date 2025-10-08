from contextlib import contextmanager
from datetime import UTC, datetime
from typing import Generic, List, Literal, TypeVar, cast, overload

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base, object_session, sessionmaker

from app.config import settings
from app.utils.convert_mixin import DictMixin

Base = declarative_base()
T = TypeVar("T", bound="BaseModel")

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_depend_db():
    db = SessionMaker()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


# 获取数据库会话的依赖函数
@contextmanager
def get_denpend_db():
    return get_depend_db()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )


class ModelMixin(Generic[T], DictMixin):
    id: Column[int | str]

    @property
    def db(self) -> Session:
        return object_session(self)

    @overload
    @classmethod
    def query(cls, db: Session, *, first: Literal[True], **kwargs) -> T | None: ...

    @overload
    @classmethod
    def query(
        cls, db: Session, *, first: Literal[False], **kwargs
    ) -> List[T] | None: ...

    @overload
    @classmethod
    def query(cls, db: Session, **kwargs) -> List[T] | None: ...

    @classmethod
    def query(cls, db: Session, *, first: bool = False, **kwargs) -> List[T] | T | None:
        skip = kwargs.pop("skip", 0)
        limit = kwargs.pop("limit", None)
        order_by = kwargs.pop("order_by", "id")
        order_desc = kwargs.pop("order_desc", True)

        query = db.query(cls)
        for key, value in kwargs.items():
            if not hasattr(cls, key):
                continue

            if isinstance(value, dict):
                operator = value.get("operator", "=")
                val = value.get("value", None)
            else:
                operator = "="
                val = value

            if operator == "!=":
                query = query.filter(getattr(cls, key) != val)
            elif operator == ">":
                query = query.filter(getattr(cls, key) > val)
            elif operator == "<":
                query = query.filter(getattr(cls, key) < val)
            elif operator == ">=":
                query = query.filter(getattr(cls, key) >= val)
            elif operator == "<=":
                query = query.filter(getattr(cls, key) <= val)
            elif operator == "in":
                query = query.filter(getattr(cls, key).in_(val))
            elif operator == "not in":
                query = query.filter(getattr(cls, key).notin_(val))
            elif operator == "like":
                query = query.filter(getattr(cls, key).like(f"%{val}%"))
            elif operator == "not like":
                query = query.filter(getattr(cls, key).notlike(f"%{val}%"))
            elif operator == "between":
                assert isinstance(val, (list, tuple)) and len(val) == 2
                query = query.filter(getattr(cls, key).between(val[0], val[1]))
            elif operator == "is null":
                query = query.filter(getattr(cls, key).is_(None))
            elif operator == "is not null":
                query = query.filter(getattr(cls, key).isnot_(None))
            elif operator == "is empty":
                query = query.filter(
                    (getattr(cls, key) == "") | (getattr(cls, key).is_(None))
                )
            elif operator == "is not empty":
                query = query.filter(
                    (getattr(cls, key) != "") & (getattr(cls, key).isnot(None))
                )
            else:
                query = query.filter(getattr(cls, key) == val)

        query = query.order_by(
            getattr(cls, order_by).desc()
            if order_desc
            else getattr(cls, order_by).asc()
        ).offset(skip)
        if first:
            if result := query.limit(1).first():
                return cast(T, result)
            return None
        if limit:
            query = query.limit(limit)
        if result := query.all():
            return cast(List[T], result)
        return None

    @classmethod
    def get_by_id(cls, db: Session, id: int | str) -> T | None:
        result = db.get(cls, id)
        if result is not None:
            return cast(T, result)
        return None

    @classmethod
    def create(cls, db: Session, ignore_id: bool = True, **kwargs) -> T:
        kwargs = {
            k: v
            for k, v in kwargs.items()
            if hasattr(cls, k) and (not ignore_id or k != "id")
        }
        kwargs["created_at"] = datetime.now(UTC)
        kwargs["updated_at"] = datetime.now(UTC)

        obj = cls(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return cast(T, obj)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in ["id", "created_at", "updated_at"]:
                continue
            elif not hasattr(self, key):
                continue
            elif getattr(self, key) != value:
                setattr(self, key, value)

        self.updated_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(self)

    def delete(self):
        self.db.delete(self)
        self.db.commit()
