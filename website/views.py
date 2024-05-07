# Stores Website URLs
from datetime import datetime

from flask import Blueprint, render_template, request, flash, \
    redirect, url_for  # views can be defined in multiple files using Blueprint
from flask_login import login_required, current_user

from . import db
from .models import Car, Reservation, User, Location

views = Blueprint('views', __name__)  # blueprint setup


@views.route('/', methods=['GET'])
def home():
    location_id = request.args.get('location')
    manufacturer = request.args.get('manufacturer')
    mileage_min = request.args.get('mileage_min')
    mileage_max = request.args.get('mileage_max')
    price_min = request.args.get('price_min')
    price_max = request.args.get('price_max')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    cars = Car.query
    if location_id:
        cars = cars.filter_by(location_id=location_id)
    if manufacturer:
        cars = cars.filter(Car.make.ilike(f'%{manufacturer}%'))
    if mileage_min:
        cars = cars.filter(Car.mileage >= mileage_min)
    if mileage_max:
        cars = cars.filter(Car.mileage <= mileage_max)
    if price_min:
        cars = cars.filter(Car.price_per_hour >= price_min)
    if price_max:
        cars = cars.filter(Car.price_per_hour <= price_max)

    if start_date and end_date:
        start_datetime = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')

        # Exclude cars with overlapping reservations
        reserved_car_ids = db.session.query(Reservation.car_id).filter(
            Reservation.pickup_time < end_datetime,
            Reservation.dropoff_time > start_datetime
        ).distinct().all()

        cars = cars.filter(Car.id.notin_([id for id, in reserved_car_ids]))

    locations = Location.query.all()
    manufacturers = [car.make for car in Car.query.distinct(Car.make)]
    location = Location.query.get(location_id) if location_id else None

    return render_template('home.html', cars=cars, locations=locations, manufacturers=manufacturers,
                           location=location, manufacturer=manufacturer,
                           mileage_min=mileage_min, mileage_max=mileage_max,
                           price_min=price_min, price_max=price_max,
                           start_date=start_date, end_date=end_date)


@views.route('/payment/<int:car_id>', methods=['GET', 'POST'])
@login_required
def payment(car_id):
    car = Car.query.get_or_404(car_id)
    user = current_user

    if request.method == 'POST':
        if not user.card_num or not user.cvv or not user.exp_date:
            flash('Please update your card information in your profile before making a reservation.', 'error')
            return redirect(url_for('auth.profile'))

        # Process the form data and create a new reservation
        pickup_date = request.form.get('pickup-date')
        pickup_time = request.form.get('pickup-time')
        dropoff_date = request.form.get('dropoff-date')
        dropoff_time = request.form.get('dropoff-time')

        # Combine the date and time values
        pickup_datetime = datetime.strptime(pickup_date + ' ' + pickup_time, '%Y-%m-%d %H:%M')
        dropoff_datetime = datetime.strptime(dropoff_date + ' ' + dropoff_time, '%Y-%m-%d %H:%M')

        # Calculate the reservation length in hours
        reservation_length = (dropoff_datetime - pickup_datetime).total_seconds() / 3600

        # Calculate the total price based on the reservation length and car's price per hour
        price = reservation_length * car.price_per_hour

        # Create a new reservation
        reservation = Reservation(
            user=user,
            car=car,
            pickup_time=pickup_datetime,
            dropoff_time=dropoff_datetime,
            reservation_length=reservation_length,
            price=price
        )
        db.session.add(reservation)
        db.session.commit()

        flash('Reservation created successfully!', 'success')
        return redirect(url_for('views.reservations'))

    return render_template('payment.html', car=car, user=user)

@views.route('/reservations')
@login_required
def reservations():
    current_reservations = Reservation.query.filter(
        Reservation.user == current_user,
        Reservation.pickup_time > datetime.now()
    ).all()

    past_reservations = Reservation.query.filter(
        Reservation.user == current_user,
        Reservation.pickup_time <= datetime.now()
    ).all()

    return render_template('reservations.html', current_reservations=current_reservations, past_reservations=past_reservations)