from datetime import datetime
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(100), nullable=False)
	name = db.Column(db.String(100), nullable=False)
	#build relationship with job
	jobs = db.relationship('Job', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.name}','{self.email}','{self.password}')"

class Job(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	program = db.Column(db.String(100), nullable=False)
	company = db.Column(db.String(100), nullable=False)
	deadline = db.Column(db.DateTime)
	#build relationship with the user
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	#build relationship with task
	tasks = db.relationship('Task', backref='position', lazy=True)

	def __repr__(self):
		return f"Job('{self.program}','{self.company}','{self.deadline}')"

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	item = db.Column(db.String(100), nullable=False)
	notes = db.Column(db.Text)
	due = db.Column(db.DateTime)
	complete = db.Column(db.Boolean(False), nullable=False)
	#build relationship with job
	job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
	
	def __repr__(self):
		return f"Task('{self.item}','{self.due}','{self.complete}')"




