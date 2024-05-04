from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import login_manager, LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'changeKeyLater' # encrypt cookies <-- we will have to hide this key locally
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # sqlite DB stored in website folder
    db.init_app(app)

    from .views import views
    from .auth import auth

    # Define prefix for route if you want
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    # need to import ALL CLASSES
    from .models import User, Car, Location, Reservation

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Where flask redirects if user not logged in
    login_manager.init_app(app)

    @login_manager.user_loader # Tells flask how we load a user
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    with app.app_context():
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            print('Created Database!')
        else:
            print('Database already exists!')