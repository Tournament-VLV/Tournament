#pip install flask
#pip install python-dotenv
#set FLASK_APP=tournament.py
#flask run
#pip install flask-sqlalchemy
#creating db in python terminal: python, from tournament import db, db.create_all()
#adding elements in console to db: from tournament import Item, item1 = Item(name="Qamas", surname="Q", points=6) , db.session.add(item1), db.session.commit
#checking items in db: Item.query.all()
from operator import length_hint
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tournament.db'
app.config['SECRET_KEY'] = '0e226e3abaa2291adf5e0fd3'
db = SQLAlchemy(app)

from tournament import routes