# Flask Authentication for login
from flask import Blueprint, render_template, request, flash, redirect, url_for  # views can be defined in multiple files

from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash # password hashing

auth = Blueprint('auth', __name__)  # blueprint setup


@auth.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email= email, first_name = first_name, password = generate_password_hash(password1, method='pbkdf2:sha256')) # sha256 is a hashing algorithm
            db.session.add(new_user)  # add user
            db.session.commit()  # update DB with changes
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))  # send user to home page

    return render_template("sign_up.html")

