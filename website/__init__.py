#DB - App Configuration'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import login_manager,LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'flaskgroupproject'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix = "/")
    app.register_blueprint(auth,url_prefix = '/')

    from .models import User,Note

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    #Configuration of login manager////
    #Where do we need to go if we not logged in
    login_manager.init_app(app)
    #Telling which app we are using
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    create_db(app)

    return app


def create_db(app):

    with app.app_context():
        if not path.exists("/website" + DB_NAME):
            db.create_all()
