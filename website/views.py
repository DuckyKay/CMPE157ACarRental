# Stores Website URLs
from flask import Blueprint, render_template  # views can be defined in multiple files using Blueprint
from flask_login import login_required, current_user

views = Blueprint('views', __name__)  # blueprint setup

@views.route('/')
@login_required
def home():
    return render_template("home.html")