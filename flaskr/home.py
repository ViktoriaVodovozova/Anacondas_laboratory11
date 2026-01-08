from flask import Blueprint, render_template, Response, url_for, session, flash
from werkzeug.utils import redirect

bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/')
def home() -> str:
    return render_template('home.html')

@bp.route('/catalog')
def catalog() -> Response:
    return redirect(url_for('catalog.catalog'))

@bp.route('/profile')
def profile() -> Response:
    user_id = session.get('user_id', None)
    if user_id is None:
        flash('Зарегестрируйтесь, чтобы войти в профиль', 'info')
        return redirect(url_for('home.home'))
    return redirect(url_for('profile.profile', user_id=user_id))