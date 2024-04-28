# Stores Website URLs
from flask import Blueprint  # views can be defined in multiple files

views = Blueprint('views', __name__)  # blueprint setup

@views.route('/')
def home():
    return "<h1>Hello World!</h1>"