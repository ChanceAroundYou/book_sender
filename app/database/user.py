from datetime import UTC, datetime
from loguru import logger
from sqlalchemy import JSON, Column, String
from sqlalchemy.orm import relationship

from app.database.base import BaseModel, ModelMixin
from app.database.series import BookSeries
from app.database.user_book import UserBook, UserBookStatus


class UserRole:
    ADMIN = "admin"
    USER = "user"


class User(BaseModel, ModelMixin["User"]):
    __tablename__ = "users"

    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    role = Column(String(20), default=UserRole.USER)
    subscriptions = Column(JSON, default=[])

    user_books = relationship("UserBook", back_populates="user")
    books = relationship(
        "Book", secondary="user_books", viewonly=True, back_populates="users"
    )

    def to_dict(self):
        d = super().to_dict()
        d["books"] = [
            {
                "id": ub.book.id,
                "title": ub.book.title,
                "status": ub.status,
                "file_path": ub.book.file_path,
                "file_size": ub.book.file_size,
                "series": ub.book.series,
                "cover_link": ub.book.cover_link,
                # "favorite": ub.favorite,
            }
            for ub in self.user_books
        ]
        return d

    def update(self, **kwargs):
        kwargs.pop("books", None)
        kwargs.pop("user_books", None)
        super().update(**kwargs)

    def get_subscription(self, series: str):
        if not BookSeries.check_series(series):
            logger.warning(f"系列 {series} 不存在")
            return

        for subscription in self.subscriptions:
            if subscription["series"] == series:
                return subscription
        return None

    def add_subscription(
        self,
        series: str,
        subscribe_date: str = '',
    ):
        from app.database.book import Book

        if not subscribe_date:
            subscribe_date = datetime.now(UTC).strftime("%Y-%m-%d")

        subscription = self.get_subscription(series)
        if subscription and subscription["subscribe_date"] == subscribe_date:
            return

        if not BookSeries.check_series(series):
            logger.warning(f"系列 {series} 不存在")
            return

        self.update(
            subscriptions=[
                *[s for s in self.subscriptions if s["series"] != series],
                {"series": series, "subscribe_date": subscribe_date},
            ]
        )
        books = Book.query(self.db, series=series)
        for book in books:
            self.add_book(book)

    def remove_subscription(self, series: str):
        from app.database.book import Book

        subscription = self.get_subscription(series)
        if not subscription:
            return

        user_books = UserBook.query(
            self.db,
            user_id=self.id,
            book_id={
                "operator": "in",
                "value": [book.id for book in Book.query(self.db, series=series)],
            },
        )
        for user_book in user_books:
            user_book.delete()

        self.update(
            subscriptions=[s for s in self.subscriptions if s["series"] != series]
        )

    def add_book(self, book):
        if book in self.books:
            return None

        subscription = self.get_subscription(book.series)
        if not subscription:
            return None
        

        if datetime.strptime(
            subscription["subscribe_date"], "%Y-%m-%d"
        ) > datetime.strptime(book.date, "%Y-%m-%d"):
            status = UserBookStatus.DISTRIBUTED
        elif book.file_size > 0:
            status = UserBookStatus.DOWNLOADED
        else:
            status = UserBookStatus.PENDING

        user_book = UserBook.create(
            self.db, user_id=self.id, book_id=book.id, status=status
        )
        # self.update(user_books=[*self.user_books, user_book])
        return user_book

    def remove_book(self, book):
        user_book = UserBook.query(
            self.db, user_id=self.id, book_id=book.id, first=True
        )
        if user_book:
            user_book.delete()
            self.update()
            
    # def favorite_book(self, book):
    #     user_book = UserBook.query(
    #         self.db, first=True, user_id=self.id, book_id=book.id
    #     )
    #     if user_book:
    #         user_book.favorited()
    #     else:
    #         self.add_book(book, favorite=True)

    # def unfavorite_book(self, book):
    #     user_book = UserBook.query(
    #         self.db, first=True, user_id=self.id, book_id=book.id
    #     )
    #     if user_book:
    #         user_book.unfavorited()

    def delete(self):
        user_books = UserBook.query(self.db, user_id=self.id)
        for user_book in user_books:
            user_book.delete()

        super().delete()
