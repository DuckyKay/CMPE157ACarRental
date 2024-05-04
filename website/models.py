import datetime
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    phone_num = db.Column(db.String(20))
    birthday = db.Column(db.Date)
    card_num = db.Column(db.String(20))
    cvv = db.Column(db.String(4))
    exp_date = db.Column(db.Date)
    license_num = db.Column(db.String(20))
    reservations = db.relationship('Reservation', back_populates='user')

    @property
    def age(self):
        today = datetime.date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='reservations')
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    car = db.relationship('Car', back_populates='reservations')
    pickup_time = db.Column(db.DateTime)
    dropoff_time = db.Column(db.DateTime)
    reservation_length = db.Column(db.Float)
    return_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    return_location = db.relationship('Location', foreign_keys=[return_location_id])
    pickup_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    pickup_location = db.relationship('Location', foreign_keys=[pickup_location_id])
    price = db.Column(db.Float)
    payment_date = db.Column(db.DateTime)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location', back_populates='cars')
    reservations = db.relationship('Reservation', back_populates='car')
    price_per_hour = db.Column(db.Float)
    plate_num = db.Column(db.String(20))
    mileage = db.Column(db.Float)
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    photo_url = db.Column(db.String(200))


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(10))
    cars = db.relationship('Car', back_populates='location')