from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User
from app import db, bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
	return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
	email = request.form.get('email')
	password = request.form.get('password')
	
	user = User.query.filter_by(email=email).first()

	#if no user is found or the password is wrong
	if not user or not bcrypt.check_password_hash(user.password, password):
		flash('Your username or password is incorrect, please try again')
		return redirect(url_for('auth.login'))

	#when email and password matches
	login_user(user)
	return redirect(url_for('main.dashboard'))

@auth.route('/signup')
def signup():
	return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
	email = request.form.get('email')
	name = request.form.get('name')
	password = request.form.get('password')

	user = User.query.filter_by(email=email).first()

	#when the user already exists
	if user:
		flash('Email is already registered.')
		return redirect(url_for('auth.signup'))

	#when the user is new
	new_user = User(email=email, name=name, password=bcrypt.generate_password_hash(password).decode('utf-8'))
	db.session.add(new_user)
	db.session.commit()
	flash('Successfully signed up. Please log in.')
	return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.index'))

@auth.route('/request_reset', methods=['GET','POST'])
@login_required
def request_reset():
	if request.method == "POST":
		email = request.form.get('email')
		user = User.query.filter_by(email=email).first()
		if user is None:
			flash('There is no account with that email, you must register first.')
			return redirect(url_for('auth.signup'))
	return render_template('request-reset.html')

#@auth.route('')
#@login_required
#def reset():
