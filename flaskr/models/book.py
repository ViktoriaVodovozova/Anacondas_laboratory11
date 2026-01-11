from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from flaskr.database.db import Base

class Book(Base):
    __tablename__ = 'books'

    NAME_MAX_LENGTH = 30
    AUTHOR_MAX_LENGTH = 30
    ANNOTATION_MAX_LENGTH = 500
    GENRE_MAX_LENGTH = 50

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), nullable=False)
    author: Mapped[str] = mapped_column(String(AUTHOR_MAX_LENGTH), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    annotation: Mapped[str] = mapped_column(String(ANNOTATION_MAX_LENGTH), nullable=True)
    genre: Mapped[str] = mapped_column(String(GENRE_MAX_LENGTH), nullable=True)