import re
from flask import (
    Blueprint, request, redirect, url_for,
    Response, render_template, session, current_app, flash
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flaskr.models.user import User
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register() -> str | Response:
    if session.get('inapp_user_id', None) is not None:
        flash('Вы уже вошли в систему, выйдите из текущего аккаунта, чтобы создать новый', 'info')
        return redirect(url_for('home.home'))
    if request.method == 'GET':
        return render_template('registration.html')

    db: SQLAlchemy = current_app.extensions['db']
    errors = []

    email = request.form.get('email', '').strip()
    nickname = request.form.get('nickname', '').strip()
    password = request.form.get('password', '').strip()
    age = request.form.get('age', '') or None
    genre = request.form.get('genre', '') or None

    if not re.match(r'^[^@]+@[^@]+.\w+$', email):
        errors.append('Неверный e-mail')
    if not (User.NICKNAME_MIN_LENGTH <= len(nickname) <= User.NICKNAME_MAX_LENGTH):
        errors.append('Неверный nickname')
    if not password:
        errors.append('Введите пароль')
    if age is not None:
        if (not re.match(r'^\d+$', age)
                or not (User.AGE_MIN <= int(age) <= User.AGE_MAX)):
            errors.append('Неверно указан возраст')
        else:
            age = int(age)
    if genre is not None and len(genre) > User.GENRE_MAX_LENGTH:
        errors.append('Неверно указан любимый жанр')
    if errors:
        for msg in errors:
            flash(msg, 'error')
        return redirect(url_for('auth.register'))

    user = User(
        email=email,
        nickname=nickname,
        password=generate_password_hash(password),
        age=age,
        genre=genre
    )
    try:
        db.session.add(user)
        db.session.commit()
        session['inapp_user_id'] = user.id
        flash('Регистрация успешно выполнена', 'success')
        return redirect(url_for('home.home'))
    except SQLAlchemyError as e:
        db.session.rollback()
        if 'UNIQUE constraint failed' in str(e):
            flash('Пользователь с таким e-mail уже существует', 'error')
        else:
            flash('Ошибка регистрации', 'error')
        print(str(e))
        return redirect(url_for('auth.register'))

@bp.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    if session.get('inapp_user_id', None) is not None:
        flash('Вы уже вошли в систему', 'info')
        return redirect(url_for('home.home'))
    if request.method == 'GET':
        return render_template('login.html')

    db: SQLAlchemy = current_app.extensions['db']

    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    try:
        stmt = select(User).where(User.email == email)
        user = db.session.scalar(stmt)
    except SQLAlchemyError:
        db.session.rollback()
        flash('Ошибка входа', 'error')
        return redirect(url_for('auth.login'))

    if user is None:
        flash('Пользователь не найден', 'error')
        return redirect(url_for('auth.login'))
    if not check_password_hash(user.password, password):
        flash('Неверный пароль', 'error')
        return redirect(url_for('auth.login'))

    session['inapp_user_id'] = user.id
    flash('Вход успешно выполнен', 'success')
    return redirect(url_for('home.home'))