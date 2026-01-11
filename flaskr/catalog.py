from sqlalchemy import select
from flask import Blueprint, render_template, current_app, session, Response, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import redirect
from flaskr.models.book import Book
from flaskr.models.user_book import UserBook

bp = Blueprint('catalog', __name__, url_prefix='/catalog')

@bp.route('/')
def catalog() -> Response | str:
    db: SQLAlchemy = current_app.extensions['db']
    try:
        stmt = select(Book)
        catalog = db.session.scalars(stmt).all()
        return render_template('catalog.html', catalog=catalog)
    except SQLAlchemyError as _:
        db.session.rollback()
        flash('Ошибка загрузки каталога', 'error')
        return redirect(url_for('home.home'))

@bp.route('/<int:book_id>')
def book(book_id: int) -> Response | str:
    db: SQLAlchemy = current_app.extensions['db']
    try:
        book = db.session.get_one(Book, book_id)
        return render_template('book.html', book=book)
    except SQLAlchemyError as _:
        db.session.rollback()
        flash('Книга не найдена в общем каталоге', 'info')
        return redirect(url_for('home.home'))

@bp.route('/<int:book_id>/add_book', methods=['POST'])
def add_book(book_id: int) -> Response:
    db: SQLAlchemy = current_app.extensions['db']

    user_id = session.get('inapp_user_id', None)
    if user_id is None:
        flash('Войдите в систему для возможности добавления книг в личный каталог', 'info')
        return redirect(url_for('catalog.book', book_id=book_id))

    try:
        user_book = db.session.get(UserBook, (user_id, book_id))
        if user_book is not None:
            flash('Книга уже находится в личном каталоге', 'info')
        else:
            user_book = UserBook(user_id=user_id, book_id=book_id)
            db.session.add(user_book)
            db.session.commit()
            flash('Книга добавлена в личный каталог', 'success')
        return redirect(url_for('catalog.book', book_id=book_id))
    except SQLAlchemyError as _:
        db.session.rollback()
        flash('Ошибка добавления книги в личный каталог', 'error')
        return redirect(url_for('catalog.catalog'))

