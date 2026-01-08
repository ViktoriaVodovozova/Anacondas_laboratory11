from flask import Blueprint, current_app, render_template, request, url_for, Response, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import redirect
from flaskr.models.book import Book
from flaskr.models.user import User
from flaskr.models.user_book import UserBook

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/<int:user_id>')
def profile(user_id: int) -> Response | str:
    db: SQLAlchemy = current_app.extensions['db']

    session_user_id = session.get('user_id', None)
    error = False
    if session_user_id is None:
        flash('Зарегестрируйтесь, чтобы просматривать профиль')
        error = True
    elif user_id != session_user_id:
        flash('У вас нет прав зелезать в чужую шкуру')
        error = True
    if error:
        return redirect(url_for('home.home'))

    user = db.session.get_one(User, user_id)
    stmt = (
        select(
            Book.id, Book.name, Book.author,
            UserBook.rating, UserBook.review
        )
        .join(UserBook, UserBook.book_id == Book.id)
        .where(UserBook.user_id == user_id)
    )
    user_books = db.session.execute(stmt).all()

    return render_template('profile.html',
                           user_id=user_id,
                           email=user.email,
                           nickname=user.nickname,
                           user_books=user_books)

@bp.route('/<int:user_id>/update_book/<int:book_id>', methods=['POST'])
def update_book(user_id: int, book_id: int) -> Response:
    db: SQLAlchemy = current_app.extensions['db']

    session_id = session.get('user_id', None)
    if session_id is None or user_id != session_id:
        return redirect(url_for('profile.profile', user_id=user_id))

    user_book = db.session.get_one(UserBook, (user_id, book_id))
    if user_book is None:
        flash('Книга либо не существует, либо не добавлена в профиль', 'info')
        return redirect(url_for('profile.profile', user_id=user_id))

    new_rating = request.form.get('rating', None)
    new_review = request.form.get('review', None)

    try:
        user_book.rating = new_rating
        user_book.review = new_review
        db.session.commit()
        flash('Отзыв сохранен', 'success')
        return redirect(url_for('profile.profile', user_id=user_id))
    except SQLAlchemyError as _:
        db.session.rollback()
        flash('Ошибка добавления', 'error')
        return redirect(url_for('profile.profile', user_id=user_id))

@bp.route('/<int:user_id>/delete_book/<int:book_id>', methods=['POST'])
def delete_book(user_id: int, book_id: int) -> Response:
    db: SQLAlchemy = current_app.extensions['db']

    session_id = session.get('user_id', None)
    if session_id is None or user_id != session_id:
        return redirect(url_for('profile.profile', user_id=user_id))

    user_book = db.session.get_one(UserBook, (user_id, book_id))
    if user_book is None:
        flash('Книга либо не существует, либо не добавлена в личный каталог', 'info')
        return redirect(url_for('profile.profile', user_id=user_id))

    try:
        db.session.delete(user_book)
        db.session.commit()
        flash('Книга удалена из персонального каталога', 'success')
        return redirect(url_for('profile.profile', user_id=user_id))
    except SQLAlchemyError as _:
        flash('Ошибка удаления', 'error')
        return redirect(url_for('profile.profile', user_id=user_id))


