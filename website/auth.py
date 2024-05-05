# Flask Authentication for login
import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for, session  # views can be defined in multiple files
from . import db
from .models import User, Location, Reservation, Car
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

@auth.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'CARRENTER1':
            session['admin_logged_in'] = True
            return redirect(url_for('auth.admin_dashboard'))
        else:
            return "Invalid password. Please try again."
    return render_template('admin_login.html')

@auth.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('auth.admin_login'))

    locations = Location.query.all()
    cars = Car.query.all()
    reservations = Reservation.query.all()
    users = User.query.all()

    return render_template('admin_dashboard.html', locations=locations, cars=cars, reservations=reservations, users=users)

@auth.route('/add-location', methods=['POST'])
def add_location():
    city = request.form.get('city')
    state = request.form.get('state')
    zip_code = request.form.get('zip_code')

    new_location = Location(city=city, state=state, zip_code=zip_code)
    db.session.add(new_location)
    db.session.commit()

    return redirect(url_for('auth.admin_dashboard'))

@auth.route('/edit-location/<int:location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)

    if request.method == 'POST':
        location.city = request.form.get('city')
        location.state = request.form.get('state')
        location.zip_code = request.form.get('zip_code')
        db.session.commit()
        return redirect(url_for('auth.admin_dashboard'))

    return render_template('edit_location.html', location=location)

@auth.route('/delete-location/<int:location_id>')
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()

    return redirect(url_for('auth.admin_dashboard'))

@auth.route('/add-car', methods=['POST'])
def add_car():
    make = request.form.get('make')
    model = request.form.get('model')
    price_per_hour = request.form.get('price_per_hour')
    photo_url = request.form.get('photo_url')

    new_car = Car(make=make, model=model, price_per_hour=price_per_hour, photo_url=photo_url)
    db.session.add(new_car)
    db.session.commit()

    return redirect(url_for('auth.admin_dashboard'))

@auth.route('/edit-car/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)

    if request.method == 'POST':
        car.make = request.form.get('make')
        car.model = request.form.get('model')
        car.price_per_hour = request.form.get('price_per_hour')
        car.photo_url = request.form.get('photo_url')
        db.session.commit()
        return redirect(url_for('auth.admin_dashboard'))

    return render_template('edit_car.html', car=car)

@auth.route('/delete-car/<int:car_id>')
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()

    return redirect(url_for('auth.admin_dashboard'))

@auth.route('/add-reservation', methods=['POST'])
def add_reservation():
    user_id = request.form.get('user_id')
    car_id = request.form.get('car_id')
    pickup_time = datetime.strptime(request.form.get('pickup_time'), '%Y-%m-%dT%H:%M')
    dropoff_time = datetime.strptime(request.form.get('dropoff_time'), '%Y-%m-%dT%H:%M')
    price = request.form.get('price')

    new_reservation = Reservation(user_id=user_id, car_id=car_id, pickup_time=pickup_time, dropoff_time=dropoff_time, price=price)
    db.session.add(new_reservation)
    db.session.commit()

    return redirect(url_for('auth.admin_dashboard'))

@auth.route('/edit-reservation/<int:reservation_id>', methods=['GET', 'POST'])
def edit_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    if request.method == 'POST':
        reservation.user_id = request.form.get('user_id')
        reservation.car_id = request.form.get('car_id')
        reservation.pickup_time = datetime.strptime(request.form.get('pickup_time'), '%Y-%m-%dT%H:%M')
        reservation.dropoff_time = datetime.strptime(request.form.get('dropoff_time'), '%Y-%m-%dT%H:%M')
        reservation.price = request.form.get('price')
        db.session.commit()
        return redirect(url_for('auth.admin_dashboard'))

    return render_template('edit_reservation.html', reservation=reservation, users=User.query.all(), cars=Car.query.all())

@auth.route('/delete-reservation/<int:reservation_id>')
def delete_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()

    return redirect(url_for('auth.admin_dashboard'))

@auth.route('/add-user', methods=['POST'])
def add_user():
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    new_user = User(email=email, first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.admin_dashboard'))

@auth.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.email = request.form.get('email')
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        db.session.commit()
        return redirect(url_for('auth.admin_dashboard'))

    return render_template('edit_user.html', user=user)

@auth.route('/delete-user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('auth.admin_dashboard'))