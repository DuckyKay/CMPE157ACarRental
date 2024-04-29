# Flask Authentication for login
from flask import Blueprint, render_template  # views can be defined in multiple files

auth = Blueprint('auth', __name__)  # blueprint setup


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up')
def signup():
    return render_template('sign_up.html')
