from flaskr.models.user import User
from flask import g, Flask
import click

class DataBase:
    def __init__(self):
        self._users: list[User] = []

    def add_user(self, user: User) -> User:
        self._users.append(user)
        return user

def get_db() -> DataBase:
    if 'db' not in g:
        g.db = DataBase()
    return g.db

def close_db(e: Exception | None = None) -> None:
    g.pop('db', None)

def init_db() -> None:
    ...

@click.command('init-db')
def init_db_command() -> None:
    init_db()
    click.echo('Database\'s been initialized')

def init_db_in_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
