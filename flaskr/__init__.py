from flask import Flask, redirect, url_for, render_template
from .db import get_db
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

    @app.route('/profile')
    def profile():
        if 'user' not in session:
            return redirect(url_for('register.register'))
        user = session['user']
        return render_template(
            'profile.html',
            username=user['nickname'],
            email=user['email'],
            age=user['age'],
            favorite_genre=user['favorite_genre']
        )
    return app

# write `flask --app flaskr run --debug` in terminal to run