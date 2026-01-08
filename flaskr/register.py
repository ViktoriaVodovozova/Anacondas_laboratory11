import re

from flask import (
    Blueprint, request, redirect, url_for,
    Response, render_template, session, current_app, flash
)
from flask_sqlalchemy import SQLAlchemy
from flaskr.models.user import User
from werkzeug.security import generate_password_hash

bp = Blueprint('register', __name__, url_prefix='/register')

@bp.route('/', methods=['GET', 'POST'])
def register() -> str | Response:
    if request.method == 'GET':
        return render_template('registration.html')

    db: SQLAlchemy = current_app.extensions['db']
    errors = []

    email = request.form.get('email', '').strip()
    nickname = request.form.get('nickname', '').strip()
    password = request.form.get('password', '').strip()

    if not re.match(r'^[^@]+@[^@]+.\w+$', email):
        errors.append('Неверный e-mail')
    if not (3 <= len(nickname) <= 30):
        errors.append('Неверный nickname')
    if not password:
        errors.append('Введите пароль')
    if errors:
        for msg in errors:
            flash(msg, 'error')
        return redirect(url_for('register.register'))

    user = User(
        email=email,
        nickname=nickname,
        password=generate_password_hash(password)
    )
    try:
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        flash('Вы успешно зарегестрировались', 'success')
        return redirect(url_for('home.home'))
    except Exception as e:
        db.session.rollback()
        if 'UNIQUE constraint failed' in str(e):
            flash('Пользователь с таким e-mail уже существует', 'error')
        else:
            flash('Ошибка регистрации', 'error')
        return redirect(url_for('register.register'))