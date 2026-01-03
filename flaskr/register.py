from flask import Blueprint, request, redirect, url_for, Response, render_template
from flaskr import get_db
from flaskr.models.user import User

bp = Blueprint('register', __name__, url_prefix='/register')

@bp.route('/register', methods=['GET', 'POST'])
def register() -> str | Response:
    if request.method == 'GET':
        return render_template('registration.html')
    db = get_db()
    db.add_user(
        User(
            email=request.form['email'],
            nickname=request.form['nickname'],
            password=request.form['password']
        )
    )
    return redirect(url_for('home.home'))