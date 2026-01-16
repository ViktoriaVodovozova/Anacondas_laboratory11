from flask import Blueprint, render_template, Response, url_for, session, flash
from werkzeug.utils import redirect

bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/')
def home() -> str:
    user_id = session.get('inapp_user_id', None)
    is_auth = True if (user_id is not None) else False
    return render_template('home.html', is_auth=is_auth)

@bp.route('/catalog')
def catalog() -> Response:
    return redirect(url_for('catalog.catalog'))

@bp.route('/profile')
def profile() -> Response:
    user_id = session.get('inapp_user_id', None)
    if user_id is None:
        flash('Войдите в систему для просмотра профиля', 'info')
        return redirect(url_for('home.home'))
    return redirect(url_for('profile.profile', user_id=user_id))