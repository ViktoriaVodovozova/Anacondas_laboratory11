from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey
from flaskr.db import Base

class UserBook(Base):
    __tablename__ = 'user_book'

    RATING_MIN = 1
    RATING_MAX = 10
    REVIEW_MAX_LENGTH = 8192

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('books.id'), primary_key=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(REVIEW_MAX_LENGTH), nullable=True)