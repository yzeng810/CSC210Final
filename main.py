from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app import db
from models import User, Job, Task, Assessment
from datetime import datetime

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

@main.route('/preference')
@login_required
def preference():
	return render_template('preference.html', name=current_user.name)

@main.route('/account', methods=['POST'])
@login_required
def account_post():
	email = request.form.get('email')
	name = request.form.get('name')
	
	if current_user.name != name:
		current_user.name = name
		db.session.commit()
		flash('You user name has been updated!')
	#if no user is found or the password is wrong
	if current_user.email != email:
		user = User.query.filter_by(email=email).first()
		if user:
			flash('The email address has been registered! Please use another email!')
		else:
			current_user.email = email
			db.session.commit()
			flash('You email address has been updated!')

	return redirect(url_for('main.account'))

@main.route('/job/new', methods=['GET','POST'])
@login_required
def new_job():
	if request.method == "POST":
		program = request.form.get('program')
		company = request.form.get('company')
		deadline = datetime.strptime(request.form.get('deadline'), "%Y-%m-%d").date()
		resumeNotes = request.form.get('resumeNotes')
		coverletterNotes = request.form.get('coverletterNotes')
		transcriptNotes = request.form.get('transcriptNotes')
		onlineFormNotes = request.form.get('onlineFormNotes')
		job = Job(program=program, company=company, deadline=deadline, resume=False, resumeNotes=resumeNotes, coverletter=False, coverletterNotes=coverletterNotes, 
			transcript=False, transcriptNotes=transcriptNotes, onlineForm=False, onlineFormNotes=onlineFormNotes, user_id=current_user.id)
		db.session.add(job)
		db.session.commit()
		return redirect(url_for('main.job'))
	return render_template('create_job.html')

#show all the applications added by the user
@main.route('/job')
@login_required
def job():
	jobs = Job.query.filter_by(user_id=current_user.id)
	return render_template('job.html', jobs=jobs)

@main.route('/job_single/<int:job_id>')
@login_required
def job_single(job_id):
	job = Job.query.get_or_404(job_id)
	return render_template('job-single.html', job=job)

@main.route('/job_update/<int:job_id>', methods=['GET','POST'])
@login_required
def job_update(job_id):
	job = Job.query.get_or_404(job_id)
	if request.method == "POST":
		program = request.form.get('program')
		company = request.form.get('company')
		deadline = datetime.strptime(request.form.get('deadline'), "%Y-%m-%d").date()
		resumeNotes = request.form.get('resumeNotes')
		coverletterNotes = request.form.get('coverletterNotes')
		transcriptNotes = request.form.get('transcriptNotes')
		onlineFormNotes = request.form.get('onlineFormNotes')
		
		job.program = program
		job.company = company
		job.deadline = deadline
		job.resumeNotes = resumeNotes
		job.coverletterNotes = coverletterNotes
		job.transcriptNotes = transcriptNotes
		job.onlineFormNotes = onlineFormNotes
		db.session.commit()
		return redirect(url_for('main.job_single', job_id=job.id))
	
	return render_template('update_job.html', job=job)

@main.route('/job_delete/<int:job_id>', methods=['GET','POST'])
@login_required
def job_delete(job_id):
	job = Job.query.get_or_404(job_id)
	db.session.delete(job)
	db.session.commit()
	flash('Your application has been deleted')
	return redirect(url_for('main.job'))

#@main.route('/reset_password', methods=['GET','POST'])
#def reset_request():
