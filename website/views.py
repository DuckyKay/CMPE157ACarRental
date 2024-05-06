# Stores Website URLs
from flask import Blueprint, render_template, request  # views can be defined in multiple files using Blueprint
from flask_login import login_required, current_user
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

    locations = Location.query.all()
    manufacturers = [car.make for car in Car.query.distinct(Car.make)]
    location = Location.query.get(location_id) if location_id else None

    return render_template('home.html', cars=cars, locations=locations, manufacturers=manufacturers,
                           location=location, manufacturer=manufacturer,
                           mileage_min=mileage_min, mileage_max=mileage_max,
                           price_min=price_min, price_max=price_max)