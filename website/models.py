from . import db
from flask_login import UserMixin  # Flask login specific
from sqlalchemy.sql import func


class Note(db.Model):  # general schema made by the dude
    id = db.Column(db.Integer, primary_key=True)  # primary key, will increment
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # get current time

    # Foreign Key Relation, each note for each user
    # 1 to many relationship. 1 user has many nodes | many to one reuquires different implementation
    # user.id is lowercase because of SQL
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# Store different class of object (singular, inherit db.model)
# just for user, inherit from usermixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # primary key
    email = db.Column(db.String(150), unique=True)  # no user can have same email
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')  # list of different notes that each user has. Capital cuz how SQL works
