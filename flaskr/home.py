from flask import Blueprint, render_template, render_template_string, session, redirect, url_for
from flaskr.models.userbook import UserBook
from flaskr import get_db

bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/')
def home() -> str:
    return render_template('home.html')

@bp.route('/profile')
def profile():
        if 'user' not in session:
            return redirect(url_for('register.register'))
        user = session['user']
        return render_template(
            'profile.html',
            username=user['nickname'],
            email=user['email'],
            age=user['age'],
            favorite_genre=user['favorite_genre']
        )

from flaskr.models.userbook import UserBook

@bp.route('/profile/add_book/<int:book_id>', methods=['POST'])
def add_book_to_profile(book_id: int):
    if 'user' not in session:
        return redirect(url_for('register.register'))

    # Пока не знаем user_id — будем использовать email как идентификатор
    # В реальности нужно хранить user.id в session после регистрации
    user_email = session['user']['email']
    db = get_db()

    # Ищем пользователя по email (это временное решение)
    user = next((u for u in db._users if u.email == user_email), None)
    if not user:
        return "Пользователь не найден", 404

    # Создаём запись UserBook
    user_book = UserBook(user_id=user.id, book_id=book_id)
    db.add_user_book(user_book)

    return redirect(url_for('home.profile'))


@bp.route('/profile/update_review/<int:user_book_id>/<int:book_id>', methods=['POST'])
def update_user_book(user_book_id: int, book_id: int):
    if 'user' not in session:
        return redirect(url_for('register.register'))

    rating = request.form.get('rating')
    review = request.form.get('review')

    db = get_db()
    user_book = db.get_user_book(user_book_id, book_id)
    if user_book:
        if rating:
            user_book.rating = int(rating)
        if review:
            user_book.review = review

    return redirect(url_for('home.profile'))

@bp.context_processor
def inject_helpers():
    def get_book(book_id):
        db = get_db()
        return db.get_book(book_id)

    return dict(get_book=get_book)
    # return app
