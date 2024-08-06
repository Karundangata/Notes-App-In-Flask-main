from flask import Blueprint,render_template, request,flash, redirect, url_for
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
import json


auth = Blueprint('auth', __name__)



@auth.route('login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		user = User.query.filter_by(email=email).first()
		# if email is already in the database
		if user:
			# if password entered matches passoword in the database 
			if check_password_hash(user.password, password):
				message = 'Logged in succesfully!'
				flash(message, category='success')
				login_user(user, remember=True)
				return redirect(url_for('views.home'))
			# if password entered does not match passoword in the database 
			elif not check_password_hash(user.password, password):
				message = 'Password entered is incorrect'
				flash(message, category='error')

		# else they should signup
	# message = 'You do not have an account. Try signing up instead'
	# flash(message, category='success')

	return render_template('login.html', user=current_user)

@auth.route('sign-up', methods=['GET','POST'])
def signup():
	# ensure your signing in
	if request.method == 'POST':
		# get info from the form
		email = request.form.get('email')
		username = request.form.get('username')
		password = request.form.get('password')
		password2 = request.form.get('password2')

		user = User.query.filter_by(email=email).first()
		# validate info from the form
		if user:
			message = 'User already exists!'
			flash(message, category='error')
		elif len(email) < 10 or len(username) < 1:
			message1 = 'email address'
			message2 = 'username'
			flash(f'You either entered an invalid {message1} or {message2}', category='error')
		elif len(password) < 4 or password != password2:
			message1 = 'too short'
			message2 = 'they do not match'
			flash(f'Your password information is either {message1} or {message2}',category='error')
		else:
			message = 'Account created succesfully'
			# new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
			new_user = User(email=email, username=username, password=generate_password_hash(password))
			db.session.add(new_user)	#add new user to database
			db.session.commit()	#commit and save changes made
			flash(message, category='success')
			login_user(new_user) 
			return redirect(url_for('views.home'))

	return render_template('signup.html', user=current_user)

@auth.route('logout')
@login_required		#ensure only logged in users accs this
def logout():
	logout_user()
	return redirect(url_for('auth.login'))	#redirect to login page


# define and protect the admin route
@auth.route('admin')
@login_required
def admin():
	return 'Admin Page'


