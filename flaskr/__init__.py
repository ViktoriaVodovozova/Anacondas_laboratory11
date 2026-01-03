from flask import Flask, redirect, url_for
from flaskr.db import get_db

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from . import (
        db,
        home, register, catalog
    )
    db.init_db_in_app(app)
    app.register_blueprint(home.bp)
    app.register_blueprint(register.bp)
    app.register_blueprint(catalog.bp)

    @app.route('/')
    def base():
        return redirect(url_for('register.register'))

    return app

# write `flask --app flaskr run --debug` in terminal to run