from os.path import exists

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
import os

if __name__ == '__main__':
    bdir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(bdir, "app_database.db")
    test_config = {
        'SECRET_KEY': 'dev',
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}'
    }
    app = create_app(test_config)
    with app.app_context():
        db: SQLAlchemy = app.extensions['db']
        if not os.path.exists(db_path):
            db.create_all()
            from flaskr.database.db import init_db_command
            init_db_command()
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )