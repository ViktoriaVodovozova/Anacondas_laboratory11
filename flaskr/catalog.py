from sqlalchemy import select
from flask import Blueprint, render_template, current_app
from flask_sqlalchemy import SQLAlchemy
from flaskr.models.book import Book

bp = Blueprint('catalog', __name__, url_prefix='/catalog')

@bp.route('/')
def catalog() -> str:
    db: SQLAlchemy = current_app.extensions['db']
    stmt = select(Book)
    catalog = db.session.scalars(stmt).all()
    return render_template('catalog.html', catalog=catalog)

@bp.route('/<int:book_id>')
def book(book_id: int) -> str:
    db: SQLAlchemy = current_app.extensions['db']
    stmt = select(Book).where(Book.id == book_id)
    book = db.session.scalar(stmt)
    return render_template('book.html', book=book)