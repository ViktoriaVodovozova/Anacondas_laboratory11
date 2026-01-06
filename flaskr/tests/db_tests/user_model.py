import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flaskr.db import create_db
from flaskr.models.user import User

class UserModelTests(unittest.TestCase):
    db = create_db()

    def setUp(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db = UserModelTests.db
        db.init_app(app)
        with app.app_context():
            db.create_all()
        app.extensions['db'] = db
        self.app = app

    def tearDown(self):
        db = self.app.extensions.pop('db')
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_fetch_user(self):
        user = User(email='simple@email.com', nickname='user', password='123')
        db: SQLAlchemy = self.app.extensions['db']
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
            db.session.remove()
        with self.app.app_context():
            stmt = select(User).where(User.id == 1)
            fetched_user = db.session.scalar(stmt)
            self.assertEqual(fetched_user.nickname, 'user')

    def test_add_fetch_users(self):
        users = [
            User(email=f'user{i}@email.com',
                 nickname=f'user{i}',
                 password=f'{i}')
            for i in range(1, 4)
        ]
        db: SQLAlchemy = self.app.extensions['db']
        with self.app.app_context():
            db.session.add_all(users)
            db.session.commit()
            db.session.remove()
        with self.app.app_context():
            stmt_by_id = select(User).where(User.id == 3)
            stmt_by_email = select(User).where(User.email == 'user3@email.com')

            fetched_by_id_user3 = db.session.scalar(stmt_by_id)
            fetched_by_email_user3 = db.session.scalar(stmt_by_email)

            self.assertListEqual(
                [fetched_by_id_user3.nickname, fetched_by_email_user3.nickname],
                ['user3'] * 2
            )
