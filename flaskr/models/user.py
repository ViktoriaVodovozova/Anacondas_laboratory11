from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from flaskr.db import Base

class User(Base):
    __tablename__ = 'users'

    EMAIL_MAX_LENGTH = 30
    NICKNAME_MIN_LENGTH = 3
    NICKNAME_MAX_LENGTH = 30
    PASSWORD_MAX_LENGTH = 150
    AGE_MIN = 10
    AGE_MAX = 120
    GENRE_MAX_LENGTH = 50

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(EMAIL_MAX_LENGTH), unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String(NICKNAME_MAX_LENGTH), nullable=False)
    password: Mapped[str] = mapped_column(String(PASSWORD_MAX_LENGTH), nullable=False)  # it should be hash
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    genre: Mapped[str] = mapped_column(String(GENRE_MAX_LENGTH))