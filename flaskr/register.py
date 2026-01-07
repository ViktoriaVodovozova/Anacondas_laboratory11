from flask import Blueprint, request, redirect, url_for, Response, render_template, session, current_app
from flask_sqlalchemy import SQLAlchemy
from flaskr.models.user import User
from werkzeug.security import generate_password_hash

bp = Blueprint('register', __name__, url_prefix='/register')

@bp.route('/', methods=['GET', 'POST'])
def register() -> str | Response:
    if request.method == 'GET':
        return render_template('registration.html')
    db: SQLAlchemy = current_app.extensions['db']
    email = request.form['email']
    nickname = request.form['nickname']
    password = request.form['password']
    user = User(email=email, nickname=nickname, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    session['user_id'] = user.id
    return redirect(url_for('home.home'))