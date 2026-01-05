from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from flaskr.db import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    nickname: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(150))  # it should be hash