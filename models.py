from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from app import app, db

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(100), nullable=False)
	name = db.Column(db.String(100), nullable=False)

	#build relationship with job and task
	jobs = db.relationship('Job', backref='author', lazy=True)
	#build relationship with task
	tasks = db.relationship('Task', backref='author', lazy=True)
	#build relationship with assessment
	#assessments = db.relationship('Assessment', backref='author', lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.name}','{self.email}','{self.password}')"

class Job(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	program = db.Column(db.String(100), nullable=False)
	company = db.Column(db.String(100), nullable=False)
	deadline = db.Column(db.DateTime)
	#complete = db.Column(db.Boolean(False), nullable=False)

	#default items to be submitted for an application - predefined in the database so that the user don't need to create each time
	resume = db.Column(db.Boolean(False), nullable=False)
	resumeNotes = db.Column(db.Text)
	coverletter = db.Column(db.Boolean(False), nullable=False)
	coverletterNotes = db.Column(db.Text)
	transcript = db.Column(db.Boolean(False), nullable=False)
	transcriptNotes = db.Column(db.Text)
	onlineForm = db.Column(db.Boolean(False), nullable=False)#online application form whether filled out or not
	onlineFormNotes = db.Column(db.Text)

	#build relationship with the user
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	#build relationship with task
	tasks = db.relationship('Task', backref='position', lazy=True)
	#build relationship with task
	assessments = db.relationship('Assessment', backref='position', lazy=True)

	def __repr__(self):
		return f"Job('{self.program}','{self.company}','{self.deadline}','{self.resume}','{self.coverletter}','{self.transcript}', '{self.onlineForm}')"

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	item = db.Column(db.String(100), nullable=False) #title of this task
	notes = db.Column(db.Text)
	due = db.Column(db.DateTime)
	complete = db.Column(db.Boolean(False), nullable=False)

	#build relationship with job
	job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
	#build relationship with the user
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return f"Task('{self.item}','{self.due}','{self.complete}')"

class Assessment(db.Model): #interview or online assessment
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False) #name of this interview E.G. 1st-round interview
	time = db.Column(db.DateTime, nullable=False) #scheduled time of this interview
	place = db.Column(db.Text) #location where the interview takes place E.G. physical address/online zoom room link and passcode
	iFormat = db.Column(db.String(100)) #online assessment/interview/group interview...
	notes = db.Column(db.String(100)) #any notes about this assessment 
	#complete = db.Column(db.Boolean(False), nullable=False)
	
	#build relationship with job
	job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
	#build relationship with user
	#user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	def __repr__(self):
		return f"Assessment('{self.title}','{self.time}','{self.iFormat}')"


