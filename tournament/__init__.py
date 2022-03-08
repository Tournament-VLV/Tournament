#pip install flask
#pip install python-dotenv
#set FLASK_APP=tournament.py
#flask run
#pip install flask-sqlalchemy
#creating db in python terminal: python, from tournament import db, db.create_all()
#adding elements in console to db: from tournament import Item, item1 = Item(name="Qamas", surname="Q", points=6) , db.session.add(item1), db.session.commit
#checking items in db: Item.query.all()
#pip install flask_bcrypt
#pip install flask_login
#python -m pip install SomePackage
import imp
from operator import length_hint
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tournament.db'
app.config['SECRET_KEY'] = '0e226e3abaa2291adf5e0fd3'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
from tournament import routes
