# Flask Authentication for login
from flask import Blueprint  # views can be defined in multiple files

auth = Blueprint('auth', __name__)  # blueprint setup


@auth.route('/login')
def login():
    return "<p>Login</p>"


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up')
def signup():
    return "<p>Sign Up<p>"
