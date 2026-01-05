from flaskr.models.user import User
from flaskr.models.book import Book
from flask import g, Flask, current_app
import click
from typing import Iterable
from flaskr.models.userbook import UserBook
_db = None

class DataBase:
    def __init__(self):
        self._users: list[User] = []
        self._catalog: list[Book] = []

    def init_db(self):
        book1 = Book(name='Каторга',
                     author='Валентин Пикуль',
                     year=1987,
                     annotation='',
                     genre='')
        book2 = Book(name='Свидание с Рамой',
                     author='Артур Кларк',
                     year=1973,
                     annotation='',
                     genre='')
        book3 = Book(name='Портрет Дориана Грея',
                     author='Оскар Уайльд',
                     year=1890,
                     annotation='',
                     genre=''
        )
        self.add_books([book1, book2, book3])

    def add_user(self, user: User) -> None:
        self._users.append(user)

    def add_book(self, book: Book) -> None:
        self._catalog.append(book)

    def add_books(self, books: Iterable[Book]) -> None:
        for book in books:
            self.add_book(book)

    def get_book(self, book_id: int):
        for book in self._catalog:
            if book.id == book_id:
                return book

    def get_catalog(self) -> list[Book]:
        return self._catalog.copy()

def get_db() -> DataBase:
    return current_app.db

    # Use code below with real DB
    # if 'db' not in g:
    #     g.db = DataBase()
    # return g.db

def close_db(e: Exception | None = None) -> None:
    g.pop('db', None)

def init_db() -> None:
    ...

@click.command('init-db')
def init_db_command() -> None:
    init_db()
    click.echo('Database\'s been initialized')

def init_db_in_app(app: Flask):
    global _db
    _db = DataBase()
    _db.init_db()
    app.db = _db

def __init__(self):
    self._users: list[User] = []
    self._catalog: list[Book] = []
    self._user_books: list[UserBook] = []  # ← новое поле

def add_user_book(self, user_book: UserBook) -> None:
    self._user_books.append(user_book)

def get_user_books_by_user_id(self, user_id: int) -> list[UserBook]:
    return [ub for ub in self._user_books if ub.user_id == user_id]

def get_user_book(self, user_id: int, book_id: int) -> UserBook | None:
    for ub in self._user_books:
        if ub.user_id == user_id and ub.book_id == book_id:
            return ub
    return None



    # Use code below with real DB
    # app.teardown_appcontext(close_db)
    # app.cli.add_command(init_db_command)
