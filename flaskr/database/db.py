import click
from flask import current_app, Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, func
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

def create_db() -> SQLAlchemy:
    return SQLAlchemy(model_class=Base)

def init_db_in_app(app: Flask) -> None:
    app.cli.add_command(init_db_command)

@click.command('init-db')
def init_db_command() -> None:
    db: SQLAlchemy = current_app.extensions['db']
    db.create_all()
    count = init_db_with_book_data()
    if count > 0:
        click.echo(f'Initialized DB with {count} books')
    else:
        click.echo(f'DB has already been initialized')

def init_db_with_book_data() -> int:
    from flaskr.models.book import Book
    db: SQLAlchemy = current_app.extensions['db']

    stmt = select(func.count()).select_from(Book)
    count = db.session.scalar(stmt)
    if count != 0:
        return 0

    books = [
        Book(
            name='Каторга',
            author='Валентин Пикуль',
            year=1987,
            annotation='',
            genre=''
        ),
        Book(
            name='Свидание с Рамой',
            author='Артур Кларк',
            year=1973,
            annotation='',
            genre=''
        ),
        Book(
            name='Портрет Дориана Грея',
            author='Оскар Уайльд',
            year=1890,
            annotation='',
            genre=''
        )
    ]
    db.session.add_all(books)
    db.session.commit()
    return len(books)
