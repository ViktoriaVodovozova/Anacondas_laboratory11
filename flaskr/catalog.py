from flask import Blueprint, render_template
from flaskr import get_db

bp = Blueprint('catalog', __name__, url_prefix='/catalog')

@bp.route('/')
def catalog() -> str:
    db = get_db()
    catalog = db.get_catalog()
    return render_template('catalog.html', catalog=catalog)

@bp.route('/<int:book_id>')
def book(book_id: int) -> str:
    db = get_db()
    book = db.get_book(book_id)
    return render_template('book.html', book=book)