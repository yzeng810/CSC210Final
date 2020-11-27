from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'toomuchhomework'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)
db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models import User
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from main import main as main_blueprint
app.register_blueprint(main_blueprint)