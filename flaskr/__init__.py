import os.path
from flask import Flask, redirect, url_for, Response
from flaskr.models.user_book import UserBook
from flaskr.models.user import User

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(app.instance_path, 'app_database.db')}'
    )
    os.makedirs(app.instance_path, exist_ok=True)

    from . import (
        db as dbc,
        home, auth, catalog, profile
    )
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

# write `flask --app flaskr init-db` in terminal to initialize database
# write `flask --app flaskr run --debug` in terminal to run