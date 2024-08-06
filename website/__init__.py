from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView 
from os import path

db = SQLAlchemy()
admin = Admin(name='Notes App Admin Panel', template_mode='bootstrap3')
db_name = 'database.db'


def create_app():
	# initialize your flask app
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'Th3N@rThR3meMBers'	# set up secret key to encrypt & secure our cookie sessions
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
	# themes = 'cerulean', 'cosmo', 'cyborg', 'flatly', 'darkly'
	app.config['FLASK_ADMIN_SWATCH'] = 'flatly'	#set bootswatch theme
	db.init_app(app)	#initialize our database
	admin.init_app(app)	#instatiate our admin panel


	# import the different blueprints and register them
	from .views import views
	app.register_blueprint(views, url_prefix='/')
	from .auth import auth
	app.register_blueprint(auth, url_prefix='/')

	from .models import User, Note
	create_database(app)

	# build the admin panel
	# admin.add_view(ModelView(User, db.session,category='user'))
	admin.add_view(ModelView(User, db.session))
	admin.add_view(ModelView(Note, db.session))
	

	# handling login sessions
	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))	#automatically looks for the primary key column

	return app

def create_database(app):
	with app.app_context():
		if not path.exists('website/' + db_name):
			# db.create_all(app=app)
			db.create_all()
			print('Created database')
		else:
			print('database already exists')



