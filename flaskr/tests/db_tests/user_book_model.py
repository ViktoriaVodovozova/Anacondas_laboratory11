import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, and_
from flaskr.db import create_db
from flaskr.models.user import User
from flaskr.models.book import Book
from flaskr.models.user_book import UserBook

class UserBookModelTests(unittest.TestCase):
    db = create_db()

    def setUp(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db = UserBookModelTests.db
        db.init_app(app)
        with app.app_context():
            db.create_all()
        app.extensions['db'] = db
        users = [User(email=f'user{i}@email.com', nickname=f'user{i}', password=f'{i}') for i in range(1, 4)]
        books = [Book(name=f'books{i}', author=f'author {i}', year=1800+2*i) for i in range(1, 6)]
        with app.app_context():
            db.session.add_all(users)
            db.session.add_all(books)
            db.session.commit()
            db.session.remove()
        self.app = app

    def tearDown(self):
        db = self.app.extensions.pop('db')
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_user_books(self):
        db: SQLAlchemy = self.app.extensions['db']
        with self.app.app_context():
            stmt_user = select(User).where(User.id == 1)
            user_id = db.session.scalar(stmt_user).id

            stmt_books = select(Book.id).where(Book.id % 2 == 1)
            books_ids = db.session.scalars(stmt_books).all()

            user_book = [UserBook(user_id=user_id, book_id=book_id) for book_id in books_ids]
            db.session.add_all(user_book)
            db.session.commit()
            db.session.remove()
        with self.app.app_context():
            stmt_books_ids = select(UserBook.book_id)
            books_ids = db.session.scalars(stmt_books_ids).all()
            self.assertEqual(len(books_ids), 3)

            stmt = (
                select(Book)
                .join(UserBook, UserBook.book_id == Book.id)
                .where(UserBook.user_id == user_id)
            )
            user_books = db.session.scalars(stmt).all()
            for i in range(3):
                self.assertEqual(user_books[i].author, f'author {2*i+1}')

