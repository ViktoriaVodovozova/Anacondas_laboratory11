from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from flaskr.db import Base

class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    author: Mapped[str] = mapped_column(String(30), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    annotation: Mapped[str] = mapped_column(String(300), nullable=True)
    genre: Mapped[str] = mapped_column(String(50), nullable=True)