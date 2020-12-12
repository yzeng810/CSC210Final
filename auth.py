from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User
from app import app, db, bcrypt, mail
from flask_mail import Message

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
def request_reset():
	if request.method == "POST":
		email = request.form.get('email')
		user = User.query.filter_by(email=email).first()
		if user is None:
			flash('There is no account with that email, you must register first.')
			return redirect(url_for('auth.signup'))
		else:
			token = user.get_reset_token()
			msg = Message('Password Reset Request', sender='noreply@offertracer.com', recipients=[user.email])
			msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
			mail.send(msg)
			flash('An email has been sent with instructions to reset your password')
			return redirect(url_for('auth.login'))
	return render_template('request-reset.html')

@auth.route('/request_reset/<token>', methods=['GET','POST'])
def reset_token(token):
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token')
		return redirect(url_for('auth.request_reset'))
	if request.method == "POST":
		password = request.form.get('password')
		verify = request.form.get('verify')
		if password == verify:
			hashed_password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
			user.password = hashed_password
			db.session.commit()
			flash('Your password has been updated')
			return redirect(url_for('auth.login'))
		else:
			flash('The password and verify password field do not match')
	return render_template('reset-password.html')
