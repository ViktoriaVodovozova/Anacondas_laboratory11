from flask import Blueprint, render_template, render_template_string

bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/')
def home() -> str:
    return render_template('home.html')

@bp.route('/profile')
def profile():
    ...
    # TODO