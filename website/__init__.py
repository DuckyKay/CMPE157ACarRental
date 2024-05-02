from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'changeKeyLater' # encrypt cookies <-- we will have to hide this key locally

    from .views import views
    from .auth import auth

    # Define prefix for route if you want
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    return app