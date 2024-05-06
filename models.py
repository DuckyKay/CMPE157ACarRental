from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    is_located_at = db.relationship('Car', backref='location', lazy=True)

class Car(db.Model):
    car_id = db.Column(db.String(50), primary_key=True)
    model = db.Column(db.String(100))
    plate_num = db.Column(db.String(20))
    price = db.Column(db.Float)
    adds = db.Column(db.String(100))
    mileage = db.Column(db.Float)
    reserve_length = db.Column(db.String(50))
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'))
    involves = db.relationship('Reservation', backref='car', lazy=True)

class Reservation(db.Model):
    reservation_id = db.Column(db.Integer, primary_key=True)
    pickup_time = db.Column(db.DateTime)
    dropoff_time = db.Column(db.DateTime)
    return_location = db.Column(db.String(100))
    pickup_location = db.Column(db.String(100))
    payment_date = db.Column(db.DateTime)
    price = db.Column(db.Float)
    makes = db.Column(db.String(50))
    car_id = db.Column(db.String(50), db.ForeignKey('car.car_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    phone_num = db.Column(db.String(20))
    email = db.Column(db.String(100))
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    card_info = db.Column(db.String(100))
    cvv = db.Column(db.String(10))
    expiration_date = db.Column(db.DateTime)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    uses = db.relationship('Reservation', backref='user', lazy=True)

class Administrator(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))