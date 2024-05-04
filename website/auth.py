# Flask Authentication for login
import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for  # views can be defined in multiple files
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash # password hashing
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)  # blueprint setup


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter(User.email.ilike(email)).first()  # search column for entered email and return first result
        if user:
            if check_password_hash(user.password, password):  # if password matches
                flash('Logged in successfully!', 'success')
                login_user(user, remember=True) # while webserver is running. user will stay logged in until they log out
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', 'error')
        else:
            flash('Email does not exist', 'error')

    return render_template('login.html')


@auth.route('/logout')
@login_required # cannot access this route unless user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_num = request.form.get('phone_num')
        birthday = request.form.get('birthday')
        card_num = request.form.get('card_num')
        cvv = request.form.get('cvv')
        exp_date = request.form.get('exp_date')
        license_num = request.form.get('license_num')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.email.ilike(email)).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_num=phone_num,
                birthday=datetime.datetime.strptime(birthday, '%Y-%m-%d').date(),
                card_num=card_num,
                cvv=cvv,
                exp_date=datetime.datetime.strptime(exp_date, '%Y-%m-%d').date(),
                license_num=license_num,
                password=generate_password_hash(password1, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html")

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')


@auth.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    current_user.first_name = request.form.get('first_name')
    current_user.last_name = request.form.get('last_name')
    current_user.phone_num = request.form.get('phone_num')
    current_user.birthday = datetime.datetime.strptime(request.form.get('birthday'), '%Y-%m-%d').date()
    current_user.card_num = request.form.get('card_num')
    current_user.cvv = request.form.get('cvv')
    current_user.exp_date = datetime.datetime.strptime(request.form.get('exp_date'), '%Y-%m-%d').date()
    current_user.license_num = request.form.get('license_num')
    db.session.commit()
    flash('Profile updated successfully!', category='success')
    return redirect(url_for('auth.profile'))


@auth.route('/delete-account')
@login_required
def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    flash('Your account has been deleted.', category='success')
    return redirect(url_for('auth.login'))
