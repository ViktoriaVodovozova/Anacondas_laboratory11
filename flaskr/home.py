from flask import Blueprint, render_template, render_template_string, session, redirect, url_for

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
    # return app
