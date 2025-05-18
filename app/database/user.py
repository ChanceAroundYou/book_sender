from datetime import datetime, UTC
from sqlalchemy import JSON, Column, String
from sqlalchemy.orm import relationship

from app.database.base import BaseModel, ModelMixin
from app.database.user_book import UserBook, UserBookStatus


class UserRole:
    ADMIN = "admin"
    USER = "user"


class User(BaseModel, ModelMixin['User']):
    __tablename__ = "users"

    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    role = Column(String(20), default=UserRole.USER)
    subscriptions = Column(JSON, default=[])

    user_books = relationship("UserBook", back_populates="user")
    books = relationship(
        "Book",
        secondary="user_books",
        viewonly=True,
        back_populates="users"
    )

    def to_dict(self):
        d = super().to_dict()
        d["books"] = [{
            "id": ub.book.id,
            "title": ub.book.title,
            "status": ub.status,
            "file_path": ub.book.file_path,
            "file_size": ub.book.file_size,
            "category": ub.book.category
        } for ub in self.user_books]
        return d
    
    def get_subscription(self, category: str):
        for subscription in self.subscriptions:
            if subscription["category"] == category:
                return subscription
        return None

    def add_subscription(self, category: str, subscribe_date: str = datetime.now(UTC).strftime("%Y-%m-%d")):
        if self.get_subscription(category):
            return

        self.update(subscriptions=[*self.subscriptions, {
            "category": category,
            "subscribe_date": subscribe_date
        }])

    def remove_subscription(self, category: str):
        from app.database.book import Book

        subscription = self.get_subscription(category)
        if not subscription:
            return

        user_books = UserBook.query(self.db, user_id=self.id, book_id={
            "operator": "in",
            "value": [book.id for book in Book.query(self.db, category=category)]
        })
        for user_book in user_books:
            user_book.delete()

        self.update(subscriptions=[s for s in self.subscriptions if s["category"] != category])

    def add_book(self, book, is_distributed: bool = False):
        if book in self.books:
            return None

        subscription = self.get_subscription(book.category)
        if not subscription:
            return None

        if is_distributed:
            status = UserBookStatus.DISTRIBUTED
        elif datetime.strptime(subscription["subscribe_date"], "%Y-%m-%d") > datetime.strptime(book.date, "%Y-%m-%d"):
            status = UserBookStatus.DISTRIBUTED
        elif book.file_size > 0:
            status = UserBookStatus.DOWNLOADED
        else:
            status = UserBookStatus.PENDING
        
        user_book = UserBook.create(self.db, user_id=self.id, book_id=book.id, status=status)
        self.update(user_books=[*self.user_books, user_book])
        return user_book
    
    def remove_book(self, book):
        user_book = UserBook.query(self.db, user_id=self.id, book_id=book.id, first=True)
        if user_book:
            user_book.delete()
            # self.update(user_books=[ub for ub in self.user_books if ub.book_id != book.id])
            self.update()

    def delete(self):
        user_books = UserBook.query(self.db, user_id=self.id)  
        for user_book in user_books:
            user_book.delete()
        
        super().delete()
