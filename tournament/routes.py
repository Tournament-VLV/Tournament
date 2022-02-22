from re import I
from tournament import app
from flask import render_template
from tournament.models import Item
from tournament.forms import RegisterForm

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/stats')
def stats():
    items = Item.query.all()
    return render_template('stats.html', items=items) 

@app.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)