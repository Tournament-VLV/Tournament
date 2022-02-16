from re import I
from tournament import app
from flask import render_template
from tournament.models import Item

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/stats')
def stats():
    items = Item.query.all()
    return render_template('stats.html', items=items) 

