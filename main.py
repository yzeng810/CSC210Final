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

@main.route('/task', methods=['GET','POST'])
@login_required
def task():
	tasks = []
	completed = []
	data = Task.query.filter_by(user_id=current_user.id)
	jobs = Job.query.filter_by(user_id=current_user.id)
	for stuff in data:
		if stuff.complete == False:
			tasks.append(stuff)
		else:
			completed.append(stuff)
	if request.method == "POST":
		item = request.form.get('item')
		notes = request.form.get('notes')
		due = datetime.strptime(request.form.get('due'), "%Y-%m-%d").date()
		job_id = request.form.get('job')
		task = Task(item=item, notes=notes, due=due, complete=False, user_id=current_user.id, job_id=job_id)
		db.session.add(task)
		db.session.commit()
		return redirect(url_for('main.task'))
	return render_template('task.html', name=current_user.name, tasks=tasks, completed=completed, jobs=jobs, id=current_user.id)

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
		return redirect(url_for('main.job_single', job_id = job_id))
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

@main.route('/task_single/<int:task_id>')
@login_required
def task_single(task_id):
	task = Task.query.get_or_404(task_id)
	return render_template('task-single.html', task=task)

@main.route('/task_single_job/<int:task_id>')
@login_required
def task_single_job(task_id):
	task = Task.query.get_or_404(task_id)
	return render_template('task-single-job.html', task=task)
	
@main.route('/task_update/<int:task_id>', methods=['GET','POST'])
@login_required
def task_update(task_id):
	jobs = Job.query.filter_by(user_id=current_user.id)
	task = Task.query.get_or_404(task_id)
	if request.method == "POST":
		item = request.form.get('item')
		notes = request.form.get('notes')
		due = datetime.strptime(request.form.get('due'), "%Y-%m-%d").date()
		job_id = request.form.get('job')
		task.item = item
		task.notes = notes
		task.due = due
		task.job_id = job_id
		db.session.commit()
		return redirect(url_for('main.task_single', task_id=task.id))
	return render_template('update_task.html', task=task, jobs=jobs)

@main.route('/task_update_job/<int:task_id>', methods=['GET','POST'])
@login_required
def task_update_job(task_id):
	jobs = Job.query.filter_by(user_id=current_user.id)
	task = Task.query.get_or_404(task_id)
	if request.method == "POST":
		item = request.form.get('item')
		notes = request.form.get('notes')
		due = datetime.strptime(request.form.get('due'), "%Y-%m-%d").date()
		job_id = request.form.get('job')
		task.item = item
		task.notes = notes
		task.due = due
		task.job_id = job_id
		db.session.commit()
		return redirect(url_for('main.job_single', job_id=job_id))
	return render_template('update_task.html', task=task, jobs=jobs)

@main.route('/task_delete/<int:task_id>', methods=['GET','POST'])
@login_required
def task_delete(task_id):
	task = Task.query.get_or_404(task_id)
	db.session.delete(task)
	db.session.commit()
	flash('Your task has been deleted')
	return redirect(url_for('main.task'))

@main.route('/task_delete_job/<int:task_id>', methods=['GET','POST'])
@login_required
def task_delete_job(task_id):
	task = Task.query.get_or_404(task_id)
	job_id = task.job_id
	db.session.delete(task)
	db.session.commit()
	flash('Your task has been deleted')
	return redirect(url_for('main.job_single', job_id=job_id))

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

@main.route('/assessment/new', methods=['GET','POST'])
@login_required
def new_assessment():
	jobs = Job.query.filter_by(user_id=current_user.id)
	if request.method == "POST":
		title = request.form.get('title')
		time = datetime.strptime(request.form.get('time'), "%Y-%m-%d").date()
		place = request.form.get('place')
		iFormat = request.form.get('iFormat')
		notes = request.form.get('notes')
		job_id = request.form.get('job')
		assessment = Assessment(complete=False, title=title, time=time, place=place, iFormat=iFormat, notes=notes, job_id=job_id, user_id=current_user.id)
		db.session.add(assessment)
		db.session.commit()
		return redirect(url_for('main.job_single', job_id=job_id))
	return render_template('create_assessment.html', jobs=jobs)

@main.route('/assessment_update/<int:assessment_id>', methods=['GET','POST'])
@login_required
def assessment_update(assessment_id):
	jobs = Job.query.filter_by(user_id=current_user.id)
	assessment = Assessment.query.get_or_404(assessment_id)
	if request.method == "POST":
		title = request.form.get('title')
		place = request.form.get('place')
		time = datetime.strptime(request.form.get('time'), "%Y-%m-%d").date()
		notes = request.form.get('notes')
		iFormat = request.form.get('iFormat')
		job_id = request.form.get('job')
		
		assessment.title = title
		assessment.place = place
		assessment.time = time
		assessment.notes = notes
		assessment.iFormat = iFormat
		assessment.job_id = job_id
		db.session.commit()
		return redirect(url_for('main.job_single', job_id=job_id))
	
	return render_template('update_assessment.html', jobs=jobs, assessment=assessment)

@main.route('/assessment_delete/<int:assessment_id>', methods=['GET','POST'])
@login_required
def assessment_delete(assessment_id):
	assessment = Assessment.query.get_or_404(assessment_id)
	job_id = assessment.job_id
	db.session.delete(assessment)
	db.session.commit()
	flash('Your assessment has been deleted')
	return redirect(url_for('main.job_single', job_id=job_id))

@main.route('/assess_complete/<id>')
def assess_complete(id):
	assessment = Assessment.query.filter_by(id=id).first()
	job_id = assessment.job_id
	assessment.complete = True
	db.session.commit()
	return redirect(url_for('main.job_single', job_id=job_id))

@main.route('/assess_incomplete/<id>')
def assess_incomplete(id):
	assessment = Assessment.query.filter_by(id=id).first()
	job_id = assessment.job_id
	assessment.complete = False
	db.session.commit()
	return redirect(url_for('main.job_single', job_id=job_id))

@main.route('/resume/<id>')
def resume(id):
	job = Job.query.filter_by(id=id).first()
	if job.resume == False:
		job.resume = True
	else:
		job.resume = False
	db.session.commit()
	return redirect(url_for('main.job_single', job_id=id))

@main.route('/coverletter/<id>')
def coverletter(id):
	job = Job.query.filter_by(id=id).first()
	if job.coverletter == False:
		job.coverletter = True
	else:
		job.coverletter = False
	db.session.commit()
	return redirect(url_for('main.job_single', job_id=id))

@main.route('/transcript/<id>')
def transcript(id):
	job = Job.query.filter_by(id=id).first()
	if job.transcript == False:
		job.transcript = True
	else:
		job.transcript = False
	db.session.commit()
	return redirect(url_for('main.job_single', job_id=id))

@main.route('/onlineForm/<id>')
def onlineForm(id):
	job = Job.query.filter_by(id=id).first()
	if job.onlineForm == False:
		job.onlineForm = True
	else:
		job.onlineForm = False
	db.session.commit()
	return redirect(url_for('main.job_single', job_id=id))

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
			transcript=False, transcriptNotes=transcriptNotes, onlineForm=False, onlineFormNotes=onlineFormNotes, complete=False, user_id=current_user.id)
		db.session.add(job)
		db.session.commit()
		return redirect(url_for('main.job'))
	return render_template('create_job.html')

#show all the applications added by the user
@main.route('/job', methods=['GET','POST'])
@login_required
def job():
	jobs = Job.query.filter_by(user_id=current_user.id)
	assessments = Assessment.query.filter_by(user_id=current_user.id)
	if request.method == "POST":
		program = request.form.get('program')
		company = request.form.get('company')
		deadline = datetime.strptime(request.form.get('deadline'), "%Y-%m-%d").date()
		resumeNotes = request.form.get('resumeNotes')
		coverletterNotes = request.form.get('coverletterNotes')
		transcriptNotes = request.form.get('transcriptNotes')
		onlineFormNotes = request.form.get('onlineFormNotes')
		job = Job(complete=False, program=program, company=company, deadline=deadline, resume=False, resumeNotes=resumeNotes, coverletter=False, coverletterNotes=coverletterNotes, 
			transcript=False, transcriptNotes=transcriptNotes, onlineForm=False, onlineFormNotes=onlineFormNotes, user_id=current_user.id)
		db.session.add(job)
		db.session.commit()
		return redirect(url_for('main.job'))
	return render_template('job.html', jobs=jobs, name=current_user.name, assessments=assessments)

@main.route('/job_complete/<id>')
@login_required
def job_complete(id):
	job = Job.query.filter_by(id=id).first()
	if job.complete == False:
		job.complete = True
	else:
		job.complete = False
	db.session.commit()
	return redirect(url_for('main.job'))

@main.route('/job_single/<int:job_id>', methods=['GET','POST'])
@login_required
def job_single(job_id):
	job = Job.query.get_or_404(job_id)
	#assessment
	assessments = Assessment.query.filter_by(job_id=job_id)
	incomplete_assessment = []
	complete_assessment = []
	for stuff in assessments:
		if stuff.complete == False:
			incomplete_assessment.append(stuff)
		else:
			complete_assessment.append(stuff)
	#tasks 
	all_tasks = Task.query.filter_by(job_id=job_id)
	incomplete_task = []
	completed_task = []
	for stuff in all_tasks:
		if stuff.complete == False:
			incomplete_task.append(stuff)
		else:
			completed_task.append(stuff)

	if request.method == "POST":
		title = request.form.get('title')
		time = datetime.strptime(request.form.get('time'), "%Y-%m-%d").date()
		place = request.form.get('place')
		iFormat = request.form.get('iFormat')
		notes = request.form.get('notes')
		job_id = job.id
		
		assessment = Assessment(complete=False, title=title, time=time, place=place, iFormat=iFormat, notes=notes, job_id=job_id, user_id=current_user.id)
		db.session.add(assessment)
		db.session.commit()
		return redirect(url_for('main.job_single', job_id=job.id))
	return render_template('job-single.html', job=job, complete_assessment=complete_assessment, incomplete_assessment=incomplete_assessment, completed_task=completed_task, incomplete_task=incomplete_task)

@main.route('/task_complete/<id>')
def task_complete(id):
	task = Task.query.filter_by(id=id).first()
	job_id = task.job_id
	task.complete = True
	db.session.commit()
	return redirect(url_for('main.job_single', job_id=job_id))

@main.route('/task_incomplete/<id>')
def task_incomplete(id):
	task = Task.query.filter_by(id=id).first()
	job_id = task.job_id
	task.complete = False
	db.session.commit()
	return redirect(url_for('main.job_single', job_id=job_id))

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
