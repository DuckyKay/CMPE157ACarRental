# Stores Website URLs
from flask import Blueprint, render_template  # views can be defined in multiple files using Blueprint

views = Blueprint('views', __name__)  # blueprint setup

@views.route('/')
def home():
    return render_template("home.html")