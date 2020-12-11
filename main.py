from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app import db, bcrypt
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

@main.route('/task')
@login_required
def task():
	tasks = []
	completed = []
	data = Task.query.filter_by(user_id=current_user.id)
	for task in data:
		if task.complete == False:
			tasks.append(task)
		else:
			completed.append(task)
	return render_template('task.html', name=current_user.name, tasks=tasks, completed=completed)

@main.route('/task/new', methods=['GET','POST'])
@login_required
def new_task():
	jobs = Job.query.filter_by(user_id=current_user.id)
	if request.method == "POST":
		item = request.form.get('item')
		notes = request.form.get('notes')
		due = datetime.strptime(request.form.get('due'), "%Y-%m-%d").date()
		job_id = request.form.get('job')
		task = Task(item=item, notes=notes, due=due, complete=False, user_id=current_user.id, job_id=job_id)
		db.session.add(task)
		db.session.commit()
		return redirect(url_for('main.task'))
	return render_template('create_task.html', jobs=jobs)

@main.route('/complete/<id>')
def complete(id):
	task = Task.query.filter_by(id=id).first()
	task.complete = True
	db.session.commit()
	return redirect(url_for('main.task'))

@main.route('/incomplete/<id>')
def incomplete(id):
	task = Task.query.filter_by(id=id).first()
	task.complete = False
	db.session.commit()
	return redirect(url_for('main.task'))

# @main.route('/task_update/<int:task_id>', methods=['GET','POST'])
# @login_required
# def task_update(task_id):
# 	job = Job.query.get_or_404(task_id)
# 	if request.method == "POST":
# 		item = request.form.get('item')
# 		notes = request.form.get('notes')
# 		due = datetime.strptime(request.form.get('due'), "%Y-%m-%d").date()
		
# 		job.program = program
# 		job.company = company
# 		job.deadline = deadline
# 		job.resumeNotes = resumeNotes
# 		job.coverletterNotes = coverletterNotes
# 		job.transcriptNotes = transcriptNotes
# 		job.onlineFormNotes = onlineFormNotes
# 		db.session.commit()
# 		return redirect(url_for('main.job_single', job_id=job.id))
	
# 	return render_template('update_job.html', job=job)

# @main.route('/job_delete/<int:job_id>', methods=['GET','POST'])
# @login_required
# def job_delete(job_id):
# 	job = Job.query.get_or_404(job_id)
# 	db.session.delete(job)
# 	db.session.commit()
# 	flash('Your application has been deleted')
# 	return redirect(url_for('main.job'))

@main.route('/account')
@login_required
def account():
	return render_template('account.html', name=current_user.name)

@main.route('/calendar')
@login_required
def calendar():
	jobTitle = []
	jobDeadline = []
	jobs = Job.query.filter_by(user_id=current_user.id)
	for job in jobs:
		jobTitle.append(job.program)
		deadline = job.deadline
		jobDeadline.append(job.deadline)
	return render_template('calendar.html', name=current_user.name, jobTitle=jobTitle, jobDeadline=jobDeadline)

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

@main.route('/account/reset_password', methods=['POST'])
@login_required
def account_reset():
	password = request.form.get('password')
	verify = request.form.get('verify')
	if password == verify:
		current_user.password = bcrypt.generate_password_hash(password).decode('utf-8')
		db.session.commit()
		flash('Your password has been updated')
		return redirect(url_for('main.account'))
	else:
		flash('The password and verify password field do not match')
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
