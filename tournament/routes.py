from re import I
from tournament import app
from flask import render_template, redirect, url_for, flash
from tournament.models import Item, User, PlayerOnTournament
from tournament.forms import RegisterForm, LoginForm, JoinTournament, BattleForm 
from tournament import db
from flask_login import login_user, logout_user, login_required, current_user
from tournament import tournament_dates
from datetime import datetime


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/stats')
@login_required
def stats():
    items = Item.query.all()
    return render_template('stats.html', items=items) 

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are logged in as: {user_to_create.username}', category='success')
        return redirect(url_for('stats'))
    if form.errors != {}: #if there is no errors from validations
        for err_msg in form.errors.values():
            flash(f'Error with creating user: {err_msg}')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('tournament'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route("/duel")
@login_required
def duel():
    items = User.query.all()
    return render_template("duel.html", items=items)

@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/tournament', methods=['GET', 'POST'])
@login_required
def tournament():
    form_join_tournament = JoinTournament()
    if form_join_tournament.validate_on_submit(): 
        exists = db.session.query(db.session.query(PlayerOnTournament).filter_by(name=current_user.username).exists()).scalar()
        if exists == False:
            user_to_play = PlayerOnTournament(name=current_user.username, points_on_tournament=current_user.user_points, date=tournament_dates.dates[0], owner=current_user.id)
            db.session.add(user_to_play)
            db.session.commit()
            flash(f'You added {current_user.username} to a Tournament! Come back after timer will goes down to check with who do you play first Match!', category='success')
        else:
            flash(f'{current_user.username} is already added to a Tournament! Good luck and have fun!', category='danger')
    date_time_str = tournament_dates.dates[0]
    date_time_obj = datetime.strptime(date_time_str, '%B %d, %Y %H:%M:%S')
    date_now = datetime.now()
    if date_time_obj > date_now:
        return render_template('tournament.html', form_join_tournament=form_join_tournament) 
    else:
        return redirect(url_for('ontournament'))


@app.route('/ontournament', methods=['GET', 'POST'])
@login_required
def ontournament():
    battle_form = BattleForm()
    if battle_form.validate_on_submit():
        print(battle_form)
    playerontournaments = PlayerOnTournament.query.all()
    return render_template('ontournament.html', playerontournaments=playerontournaments, battle_form=battle_form)