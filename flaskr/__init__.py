import os.path
from flask import Flask, redirect, url_for, Response
from flaskr.db import init_db_in_app

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(app.instance_path, 'app_database.db')}'
    )
    os.makedirs(app.instance_path, exist_ok=True)

    from . import (
        db as dbc,
        home, register, catalog
    )
    db = dbc.create_db()
    db.init_app(app)
    app.register_blueprint(home.bp)
    app.register_blueprint(register.bp)
    app.register_blueprint(catalog.bp)
    app.extensions['db'] = db
    init_db_in_app(app)

    @app.route('/')
    def base() -> Response:
        return redirect(url_for('register.register'))

    return app

# write `flask --app flaskr init-db` in terminal to initialize database
# write `flask --app flaskr run --debug` in terminal to run