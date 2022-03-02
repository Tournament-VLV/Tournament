from email.policy import default
from tournament import db, login_manager
from tournament import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=70), unique=False, nullable=False)
    user_points = db.Column(db.Integer(), nullable=True, default=0)
    items = db.relationship('Item', backref='owned_user', lazy=True)


    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password) 


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=False)
    surname = db.Column(db.Integer(), nullable=False)
    points_on_tournament = db.Column(db.Integer(), nullable=True, unique=False, default=0)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))


    def __repr__(self):
        return f'Item {self.name}'
