import os.path

import click
from flask import Flask, redirect, url_for, Response
from flaskr.models.user_book import UserBook
from flaskr.models.user import User

def create_app(test_config: dict = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        click.echo('using test config')
        app.config.from_mapping(test_config)

    from . import (
        home, auth, catalog, profile
    )
    from flaskr.database import db as dbc
    db = dbc.create_db()
    db.init_app(app)
    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(catalog.bp)
    app.register_blueprint(profile.bp)
    app.extensions['db'] = db
    dbc.init_db_in_app(app)

    @app.context_processor
    def inject_model_constraints():
        return {
            'RATING_MIN': UserBook.RATING_MIN,
            'RATING_MAX': UserBook.RATING_MAX,
            'REVIEW_MAX_LENGTH': UserBook.REVIEW_MAX_LENGTH,
            'NICKNAME_MIN_LENGTH': User.NICKNAME_MIN_LENGTH,
            'NICKNAME_MAX_LENGTH': User.NICKNAME_MAX_LENGTH,
            'AGE_MIN': User.AGE_MIN,
            'AGE_MAX': User.AGE_MAX,
            'FAV_GENRE_MAX_LENGTH': User.GENRE_MAX_LENGTH
        }

    @app.route('/')
    def base() -> Response:
        return redirect(url_for('home.home'))

    return app
