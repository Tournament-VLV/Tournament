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
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=False)
    surname = db.Column(db.String(length=30), nullable=False, unique=False)
    points = db.Column(db.Integer(), nullable=False)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/stats')
def stats():
    items = [
    {'id': 1, 'Name': 'Kamil', 'Surname': 'K', 'Points': '3'},
    {'id': 2, 'Name': 'Mariusz', 'Surname': 'R',  'Points': '7'},
    {'id': 3, 'Name': 'Mariusz', 'Surname': 'Z', 'Points': '4'}
]
    return render_template('stats.html', items=items) 



if __name__ == "__main__":
    app.run()

