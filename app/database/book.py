from datetime import UTC, datetime
from typing import Any, Dict, Optional

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Session, relationship

from app.database.base import BaseModel, ModelMixin
from app.database.series import BookSeries
from app.database.user import User
from app.database.user_book import UserBook, UserBookStatus


class BookFormat:
    """书籍格式枚举"""

    PDF = "pdf"
    EPUB = "epub"
    MOBI = "mobi"
    TXT = "txt"


class Book(BaseModel, ModelMixin["Book"]):
    """数据库书籍模型"""

    __tablename__ = "books"

    title = Column(String(200), index=True)
    date = Column(String(100))
    author = Column(String(100))
    summary = Column(String(1000))
    cover_link = Column(String(500))
    detail_link = Column(String(500))
    download_link = Column(String(500))
    series = Column(String(100))

    file_path = Column(String(500))
    file_size = Column(Integer, default=0)
    file_format = Column(String(20), default=BookFormat.PDF)
    downloaded_at = Column(DateTime, default=lambda: datetime.now(UTC))

    # 关系定义
    user_books = relationship("UserBook", back_populates="book")
    users = relationship(
        "User", secondary="user_books", viewonly=True, back_populates="books"
    )

    def to_dict(self, obj=None, exclude=None, max_depth=5) -> Dict[str, Any]:
        """实现接口方法：转换为字典"""
        base_dict = super().to_dict(obj=obj, exclude=exclude, max_depth=max_depth)
        base_dict["users"] = [
            {
                "id": ub.user.id,
                "username": ub.user.username,
                "email": ub.user.email,
                "status": ub.status,
            }
            for ub in self.user_books
        ]
        return base_dict

    @classmethod
    def create(cls, db: Session, ignore_id: bool = True, **kwargs) -> "Book":
        """创建书籍并处理用户订阅关系"""
        title = kwargs.get("title")
        if not title:
            raise ValueError("书籍标题不能为空")
        series = BookSeries.get_series(title)
        kwargs["series"] = series

        book = super().create(db, ignore_id=ignore_id, **kwargs)
        users = User.query(db)
        if not users:
            return book

        for user in users:
            subscription = user.get_subscription(series)
            if subscription is None:
                continue

            date = str(subscription["subscribe_date"])
            status = (
                UserBookStatus.PENDING
                if datetime.strptime(book.date, "%Y-%m-%d")
                > datetime.strptime(date, "%Y-%m-%d")
                else UserBookStatus.DISTRIBUTED
            )

            user_book = UserBook.query(db, user_id=user.id, book_id=book.id, first=True)
            if not user_book:
                UserBook.create(db, user_id=user.id, book_id=book.id, status=status)
            else:
                user_book.update(status=status)

        return book

    def update(self, **kwargs):
        kwargs.pop("user_books", None)
        kwargs.pop("users", None)
        super().update(**kwargs)

    def downloaded(self, file_path: str, file_size: int, file_format: str) -> None:
        """实现接口方法：更新下载状态"""
        user_books = UserBook.query(self.db, book_id=self.id)
        if not user_books:
            return

        for user_book in user_books:
            user_book.downloaded()

        self.update(
            file_path=file_path,
            file_size=file_size,
            file_format=file_format,
            downloaded_at=datetime.now(UTC),
        )

    def distributed(
        self, user_id: Optional[int] = None, email: Optional[str] = None
    ) -> None:
        """实现接口方法：更新分发状态"""
        if not (user_id or email):
            raise ValueError("用户ID或邮箱不能都为空")

        if user_id:
            user_books = UserBook.query(self.db, book_id=self.id, user_id=user_id)
        else:
            user_books = (
                self.db.query(UserBook)
                .join(User)
                .filter((UserBook.book_id == self.id) & (User.email == email))
                .all()
            )
        if not user_books:
            return

        for user_book in user_books:
            user_book.distributed()
        self.update()

    def delete(self) -> None:
        """删除书籍及相关用户关系"""
        user_books = UserBook.query(self.db, book_id=self.id)
        if not user_books:
            return

        for user_book in user_books:
            self.db.delete(user_book)
        super().delete()
