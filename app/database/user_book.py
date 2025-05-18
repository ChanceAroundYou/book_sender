from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base import BaseModel, ModelMixin


class UserBookStatus:
    PENDING = "pending"           # 等待下载
    DOWNLOADED = "downloaded"     # 已下载
    DISTRIBUTED = "distributed"   # 已分发

class UserBook(BaseModel, ModelMixin['UserBook']):
    __tablename__ = "user_books"

    # id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    status = Column(String(20), default=UserBookStatus.PENDING)

    # 关系
    user = relationship("User", back_populates="user_books")
    book = relationship("Book", back_populates="user_books")
    
    def downloaded(self):
        if self.status == UserBookStatus.PENDING:
            self.update(status=UserBookStatus.DOWNLOADED)

    def distributed(self):
        self.update(status=UserBookStatus.DISTRIBUTED)
