from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# models = Blueprint('models', __name__)
class User(db.Model, UserMixin):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	username = db.Column(db.String(100))
	password = db.Column(db.String(100))
	notes = db.relationship('Note')

class Note(db.Model):
	__tablename__ = 'notes'
	id = db.Column(db.Integer, primary_key=True)
	data = db.Column(db.String(10000))
	date = db.Column(db.DateTime(timezone=True), default=func.now())
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))








