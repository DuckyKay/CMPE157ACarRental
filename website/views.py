# Stores Website URLs
from flask import Blueprint, render_template  # views can be defined in multiple files using Blueprint
from flask_login import login_required, current_user
from .models import Car, Reservation, User, Location

views = Blueprint('views', __name__)  # blueprint setup

@views.route('/')
@login_required
def home():
    cars = Car.query.all()
    return render_template("home.html", cars=cars)