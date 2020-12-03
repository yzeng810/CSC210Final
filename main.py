from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from models import User, Job, Task

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
	return render_template('dashboard.html', name=current_user.name)

@main.route('/account')
@login_required
def account():
	return render_template('account.html', name=current_user.name)

@main.route('/account', methods=['POST'])
def account_post():
	email = request.form.get('email')
	name = request.form.get('name')
	
	if current_user.name != name:
		current_user.name = name
		db.session.commit()
	#if no user is found or the password is wrong
	if current_user.email != email:
		user = User.query.filter_by(email=email).first()
		if user:
			flash('The email address has been registered! Please use another email!')
		else:
			current_user.email = email
			db.session.commit()

	return redirect(url_for('main.account'))