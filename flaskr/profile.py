from flask import Blueprint, current_app, render_template, request, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from werkzeug.utils import redirect
from flaskr.models.book import Book
from flaskr.models.user import User
from flaskr.models.user_book import UserBook

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/<int:user_id>')
def profile(user_id: int) -> str:
    db: SQLAlchemy = current_app.extensions['db']
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
                           email=user.email,
                           nickname=user.nickname,
                           user_books=user_books)

@bp.route('/<int:user_id>/update_book/<int:book_id>', methods=['POST'])
def update_book(user_id: int, book_id: int) -> Response:
    db: SQLAlchemy = current_app.extensions['db']
    new_rating = request.form.get('rating', None)
    new_review = request.form.get('review', None)
    user_book = db.session.get_one(UserBook, (user_id, book_id))
    user_book.rating = new_rating
    user_book.review = new_review
    db.session.commit()
    return redirect(url_for('profile.profile', user_id=user_id))


