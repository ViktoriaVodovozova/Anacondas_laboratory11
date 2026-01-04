from flask import Blueprint, request, redirect, url_for, Response, render_template, session
from flaskr import get_db
from flaskr.models.user import User

bp = Blueprint('register', __name__, url_prefix='/register')

@bp.route('/', methods=['GET', 'POST'])
def register() -> str | Response:
    if request.method == 'GET':
        return render_template('registration.html')
    db = get_db()
    email = request.form['email']
    nickname = request.form['nickname']
    password = request.form['password']
    age = request.form['age']
    favorite_genre = request.form['favorite_genre']
    user = User(email=email, nickname=nickname, password=password, age=age, favorite_genre=favorite_genre)

    # TODO session['user_id'] = user.id

    db.add_user(user)
    return redirect(url_for('home.home'))