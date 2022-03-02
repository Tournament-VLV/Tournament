from email.policy import default
from tournament import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address = db.Column(db.String(length=50), unique=True, nullable=False)
    user_password = db.Column(db.String(length=70), unique=False, nullable=False)
    user_points = db.Column(db.Integer(), nullable=True, default=0)
    items = db.relationship('Item', backref='owned_user', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=False)
    surname = db.Column(db.Integer(), nullable=False)
    points_on_tournament = db.Column(db.Integer(), nullable=True, unique=False, default=0)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

class Matches(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    data = db.Column(db.String(), nullable=False)
    oponent = db.Column(db.String(), nullable=False)
    result = db.Column(db.Integer(), nullable=True, unique=False, default=0)

    def __repr__(self):
        return f'Item {self.name}'
