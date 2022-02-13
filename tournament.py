#pip install flask
#pip install python-dotenv
#set FLASK_APP=tournament.py
#flask run
from flask import Flask, render_template

app = Flask(__name__)

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

