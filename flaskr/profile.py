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

    if not check_user_access(user_id):
        return redirect(url_for('home.home'))

    try:
        user = db.session.get(User, user_id)
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
                               user=user,
                               user_books=user_books)
    except SQLAlchemyError as _:
        db.session.rollback()
        flash('Ошибка загрузки профиля', 'error')
        return redirect(url_for('home.home'))

@bp.route('/<int:user_id>/logout')
def logout(user_id: int):
    if not check_user_access(user_id):
        return redirect(url_for('profile.profile'))
    session.pop('inapp_user_id')
    flash('Выполнен выход из системы', 'success')
    return redirect(url_for('home.home'))

@bp.route('/<int:user_id>/update_book/<int:book_id>', methods=['POST'])
def update_book(user_id: int, book_id: int) -> Response:
    db: SQLAlchemy = current_app.extensions['db']
    errors = []

    if not check_user_access(user_id):
        return redirect(url_for('home.home'))

    try:
        user_book = db.session.get(UserBook, (user_id, book_id))
    except SQLAlchemyError as _:
        db.session.rollback()
        flash('Ошибка сохранения отзыва', 'error')
        return redirect(url_for('profile.profile', user_id=user_id))

    if user_book is None:
        flash('Книга либо не существует, либо не добавлена в личный каталог', 'info')
        return redirect(url_for('profile.profile', user_id=user_id))

    new_rating = request.form.get('rating', None)
    new_review = request.form.get('review', None)

    if not isinstance(new_review, int) or not (UserBook.RATING_MIN <= new_review <= UserBook.RATING_MAX):
        errors.append('Оценка должна быть целым числом от 1 до 10')
    if len(new_review) > UserBook.REVIEW_MAX_LENGTH:
        errors.append(f'Отзыв превышает допустимое количество символов ({UserBook.REVIEW_MAX_LENGTH})')
    if errors:
        for msg in errors:
            flash(msg, 'error')
        return redirect(url_for('profile.profile', user_id=user_id))

    try:
        user_book.rating = new_rating
        user_book.review = new_review
        db.session.commit()
        flash('Отзыв успешно сохранен', 'success')
        return redirect(url_for('profile.profile', user_id=user_id))
    except SQLAlchemyError as _:
        db.session.rollback()
        flash('Ошибка сохранения отзыва', 'error')
        return redirect(url_for('profile.profile', user_id=user_id))

@bp.route('/<int:user_id>/delete_book/<int:book_id>', methods=['POST'])
def delete_book(user_id: int, book_id: int) -> Response:
    db: SQLAlchemy = current_app.extensions['db']

    if not check_user_access(user_id):
        return redirect(url_for('home.home'))

    try:
        user_book = db.session.get(UserBook, (user_id, book_id))
    except SQLAlchemyError as _:
        db.session.rollback()
        flash('Ошибка удаления книги', 'error')
        return redirect(url_for('profile.profile', user_id=user_id))

    if user_book is None:
        flash('Книга либо не существует, либо не добавлена в личный каталог', 'info')
        return redirect(url_for('profile.profile', user_id=user_id))

    try:
        db.session.delete(user_book)
        db.session.commit()
        flash('Книга успешно удалена из личного каталога', 'success')
        return redirect(url_for('profile.profile', user_id=user_id))
    except SQLAlchemyError as _:
        flash('Ошибка удаления книги', 'error')
        return redirect(url_for('profile.profile', user_id=user_id))

def check_user_access(user_id: int) -> bool:
    session_user_id = session.get('inapp_user_id', None)
    if session_user_id is None:
        flash('Войдите в систему для просмотра профиля', 'error')
        return False
    if user_id != session_user_id:
        flash('У вас нет прав зелезать в чужую шкуру', 'error')
        return False
    return True