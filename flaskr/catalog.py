from sqlalchemy import select
from flask import Blueprint, render_template, current_app, session, Response, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from flaskr.models.book import Book
from flaskr.models.user_book import UserBook

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
    book = db.session.get_one(Book, book_id)
    return render_template('book.html', book=book)

@bp.route('/<int:book_id>/add_book', methods=['POST'])
def add_book(book_id: int) -> Response:
    db: SQLAlchemy = current_app.extensions['db']
    user_id = session['user_id']
    user_book = UserBook(user_id=user_id, book_id=book_id)
    db.session.add(user_book)
    db.session.commit()
    return redirect(url_for('catalog.book', book_id=book_id))
