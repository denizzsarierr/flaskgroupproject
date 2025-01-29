#DB - App Configuration'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'flaskgroupproject'


    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix = "/")
    app.register_blueprint(auth,url_prefix = '/')


    return app


def create_db(app):

    with app.app_context():
        if not path.exists(f"/website" + {DB_NAME}):
            db.create_all()
