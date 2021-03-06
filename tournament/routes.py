from re import I

from requests import session
from tournament import app
from flask import render_template, redirect, url_for, flash, request
from tournament.models import Item, User, PlayerOnTournament
from tournament.forms import RegisterForm, LoginForm, JoinTournament, BattleForm, Battles
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
            flash(f'You added {current_user.username} to a Tournament! Come back after timer will goes down to face your opponent!', category='success')
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
        fighting_player = request.form.get('battle_player')
        if current_user.username == fighting_player:
            flash(f'You cant battle with yourself!', category='danger')
        else:
            user_B = fighting_player
            user_A = current_user.username
            if request.method == "POST":
                return redirect(url_for('battle', usrA=user_A, usrB=user_B))
    playerontournaments = PlayerOnTournament.query.all()
    return render_template('ontournament.html', playerontournaments=playerontournaments, battle_form=battle_form)

@app.route('/battle/<string:usrA>/<string:usrB>', methods=['GET', 'POST'])
@login_required
def battle(usrA, usrB):
    battles = Battles()
    scoreA = battles.goalsA.data
    scoreB = battles.goalsB.data
    playerA = usrA
    playerB = usrB

    if request.method == "POST":
        #firstCase
        if scoreA > scoreB:
            winnerA_firstCase = playerA
            looserB_firstCase = playerB
            users = User.query.all()
            for user in users:
                if user.username == winnerA_firstCase:
                    user.user_points +=10
                    user.user_played_matches +=1
                    user.user_won_matches +=1
                    db.session.commit()
            for user in users:
                if user.username == looserB_firstCase:
                    user.user_points -=6
                    user.user_played_matches +=1
                    user.user_lost_matches +=1
                    db.session.commit()
            return redirect(url_for('ontournament'))
         #secondCase
        if scoreB > scoreA:
            winnerB_secondCase = playerB
            looserA_secondCase = playerA
            users = User.query.all()
            for user in users:
                if user.username == winnerB_secondCase:
                    user.user_points +=10
                    user.user_played_matches +=1
                    user.user_won_matches +=1
                    db.session.commit()
            for user in users:
                if user.username == looserA_secondCase:
                    user.user_points -=6
                    user.user_played_matches +=1
                    user.user_lost_matches +=1
                    db.session.commit()
            return redirect(url_for('ontournament'))
        #thirdCase
        if scoreA == scoreB:
            same_scoreA = playerA
            same_scoreB = playerB
            users = User.query.all()
            for user in users:
                if user.username == same_scoreA:
                    user.user_points +=5
                    user.user_played_matches +=1
                    user.user_draws +=1
                    db.session.commit()
            for user in users:
                if user.username == same_scoreB:
                    user.user_points +=5
                    user.user_played_matches +=1
                    user.user_draws +=1
                    db.session.commit()
            return redirect(url_for('ontournament'))    
    return render_template('battle.html', battles=battles, usrA=usrA, usrB=usrB)


@app.route('/ranking')
def ranking():
    users = User.query.all()
    return render_template('ranking.html', users=users) 