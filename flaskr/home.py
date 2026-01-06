from flask import Blueprint, render_template, Response, url_for, session
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
    user_id = session['user_id']
    return redirect(url_for('profile.profile', user_id=user_id))