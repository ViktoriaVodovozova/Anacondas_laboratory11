from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey
from flaskr.db import Base

class UserBook(Base):
    __tablename__ = 'user_book'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('books.id'), primary_key=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String, nullable=True)