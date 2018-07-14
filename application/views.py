from datetime import datetime

from werkzeug.urls import url_parse
from flask_login import (
	LoginManager, current_user, login_user, logout_user, login_required)
from flask import (
	request, session, render_template, redirect, url_for, flash)

from . import app, db
from .forms import LoginForm, RegistrationForm, EditProfileForm
from .models import User, Feed

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/')
@app.route('/index/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
		# TODO:
		# [x] verify the login
		# [x] get the user id from the database
		# [ ] register the user id, name, photo, etc in the current session
		# [x] redirect to user page
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>/')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/user/')
@login_required
def profile(username):
    return redirect(url_for('user', username=current_user.username))

@app.route('/user/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template(
		'edit_profile.html', title='Edit Profile', form=form)

@app.route('/subscribe/<feed_id>')
@login_required
def subscribe(feed_id):
	feed = Feed.query.filter_by(id=feed_id).first_or_404()
	username = User.query.filter_by(id=feed.owner_id).first()
	if username == current_user.id:
		flash('You are subscribed to your feeds by default.')
		return redirect(url_for('user', username=username))
	current_user.subscribe(feed)
	db.session.commit()
	flash('You have been subscribed to {}!'.format(feed.name))
	return redirect(url_for('user', username=username))

@app.before_request
def update_last_seen():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()