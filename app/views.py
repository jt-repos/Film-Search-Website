from flask import render_template, flash, redirect
from app import app, db, models, admin
from flask_admin.contrib.sqla import ModelView
from .forms import LoginForm, RegisterForm, AddFilmForm, AddCinemaForm, AddScreeningForm, ChangePasswordForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import datetime

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
	return models.User.query.get(int(id))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user = current_user
    return render_template('dashboard.html', title='My Films', myFilms=user.favouriteFilm)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		#create a table row consisting of values from the form
		user = models.User.query.filter_by(username=form.username.data).first()
		if user:
			#check password
			if(user.password==form.password.data):
				login_user(user)
				flash('Login successful')
				app.logger.info('%s logged in successfully', user.username)
				return dashboard()
			else:
				app.logger.warning('someone tried to access account %s', user.username)
				flash('Password is incorrect')
		else:
			flash('Username incorrect')
	return render_template('login.html', title='login', form = form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	user = current_user
	app.logger.info('%s logged out successfully', user.username)
	logout_user()
	flash("You have been logged out")
	return login()

@app.route('/addFilm', methods=['GET', 'POST'])
@login_required
def addFilm():
	form = AddFilmForm()
	if form.validate_on_submit():
		#create a table row consisting of values from the form
		try:
			if(int(form.length.data) <= 0):
				flash('Invalid film length')
				return render_template('addFilm.html', title='Add Film', form=form)
			p = getFilmRow(filmName=form.filmName.data,
							length=int(form.length.data),
							releaseDate=form.releaseDate.data,
							studioName=form.studioName.data)
			db.session.add(p)
			db.session.commit()
			#feedback message on success
			flash('Film added successfully')
		except Exception as e:
		#feedback message when task failed
			flash('Failed to add film') #delete error later
	return render_template('addFilm.html', title='Add Film', form=form)

def getFilmRow(filmName, length, releaseDate, studioName):
	if(len(filmName) > 128 or len(filmName) == 0):
		return -1
	if(length <= 0):
		return -1
	if(len(studioName) > 128 or len(studioName) == 0):
		return -1
	p = models.Film(filmName=filmName,
					length=length,
					releaseDate=releaseDate,
					studioName=studioName)
	return p

@app.route('/addCinema', methods=['GET', 'POST'])
@login_required
def addCinema():
	form = AddCinemaForm()
	if form.validate_on_submit():
		#create a table row consisting of values from the form
		try:
			if(int(form.capacity.data) <= 0):
				flash('Invalid cinema capacity')
				return render_template('addCinema.html', title='Add Cinema', form=form)
			p = getCinemaRow(cinemaName=form.cinemaName.data,
							address=form.address.data,
							capacity=form.capacity.data,
							openTime=form.openTime.data,
							closeTime=form.closeTime.data)
			db.session.add(p)
			db.session.commit()
			#feedback message on success
			flash('Cinema added successfully')
		except Exception as e:
		#feedback message when task failed
			flash('Failed to add cinema') #delete error later
	return render_template('addCinema.html', title='Add Cinema', form=form)

def getCinemaRow(cinemaName, address, capacity, openTime, closeTime):
	if(len(cinemaName) > 128 or len(cinemaName) == 0):
		return -1
	if(capacity <= 0):
		return -1
	if(not isinstance(openTime, datetime.time) or not isinstance(closeTime, datetime.time)):
		return -1
	p = models.Cinema(cinemaName=cinemaName,
					address=address,
					capacity=capacity,
					openTime=openTime,
					closeTime=closeTime)
	return p

@app.route('/addScreening', methods=['GET', 'POST'])
@login_required
def addScreening():
    form = AddScreeningForm()
    if form.validate_on_submit():
        film = models.Film.query.filter_by(filmId=form.filmId.data).first()
        cinema = models.Cinema.query.filter_by(cinemaId=form.cinemaId.data).first()
        if(not(film)):
            flash('Film not found')
            return render_template('addScreening.html', title='Add Screening', form=form)
        if(not(cinema)):
            flash('Cinema not found')
            return render_template('addScreening.html', title='Add Screening', form=form)
		#create a table row consisting of values from the form
        cinema.screening.append(film)
        try:
            db.session.commit()
            flash('Screening added successfully')
            return home()
        except Exception as e:
		#feedback message when task failed
            flash('Failed to add screening')
    return render_template('addScreening.html', title='Add Screening', form=form)

@app.route('/home', methods=['GET', 'POST'])
def home():
	allFilms = models.Film.query.all()
	allCinemas = models.Cinema.query.all()
	return render_template('home.html', title='Home', films=allFilms, cinemas=allCinemas)

@app.route('/create', methods=['GET', 'POST'])
def createAccount():
    form = RegisterForm()
	#if form is successfully validated
    if form.validate_on_submit():
		#create a table row consisting of values from the form
        hasUpper = False;
        if(form.password1.data!=form.password2.data):
            flash('Passwords not matching')
            return render_template('create.html', title='Create', form=form)
        if(len(form.password1.data) < 4 or len(form.password1.data) > 32 or
            len(form.username.data) < 4 or len(form.username.data) > 32):
            flash('Username and password must be between 4 and 32 characters long')
            return render_template('create.html', title='Create', form=form)
        for letter in str(form.password1.data):
            if letter.isupper():
                hasUpper = True
        if(hasUpper == False):
            flash('Password must contain a capital letter')
            return render_template('create.html', title='Create Account', form=form)
        p = getUserRow(username=form.username.data, email=form.email.data, password=form.password1.data)

        try:
            db.session.add(p)
            db.session.commit()
			#feedback message on success
            app.logger.info('%s created a new account', form.username.data)
            flash('Account created successfully')
        except Exception as e:
			#feedback message when task failed
            flash('Failed to create the account')
    return render_template('create.html', title='Create', form=form)

def getUserRow(username, email, password):
	if(len(username) > 32 or len(username) == 0):
		return -1
	if(len(email) > 32 or len(email) == 0):
		return -1
	if(len(password) > 32 or len(password) == 0):
		return -1
	p = models.User(username=username, email=email, password=password)
	return p

@app.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    form = ChangePasswordForm()
	#if form is successfully validated
    if form.validate_on_submit():
		#create a table row consisting of values from the form
        user = current_user
        hasUpper = False;
        if(form.password.data != user.password):
            flash('Current password incorrect')
            app.logger.warning('%s tried to change his password', user.username)
            return render_template('changePassword.html', title='Change Password', form=form)
        if(form.password1.data != form.password2.data):
            flash('Passwords not matching')
            return render_template('changePassword.html', title='Change Password', form=form)
        if(len(form.password1.data) < 4 or len(form.password1.data) > 32):
            flash('Password must be between 4 and 32 characters long')
            return render_template('changePassword.html', title='Change Password', form=form)
        for letter in str(form.password1.data):
            if letter.isupper():
                hasUpper = True
        if(hasUpper == False):
            flash('Password must contain a capital letter')
            return render_template('changePassword.html', title='Change Password', form=form)

        current_user.password = form.password1.data
        try:
            db.session.commit()
			#feedback message on success
            flash('Password updated successfully')
            app.logger.info('%s updated password', user.username)
        except Exception as e:
			#feedback message when task failed
            flash('Failed to update password')
    return render_template('changePassword.html', title='Change Password', form=form)

@app.route('/markAsFavourite/<int:id>', methods=['GET', 'POST'])
@login_required
def updateFavourite(id):
    film = models.Film.query.get_or_404(id)
    user = current_user
    user.favouriteFilm.append(film)
    try:
        db.session.commit()
        flash('Added to favourite')
        return render_template('dashboard.html', title='My Films', myFilms=user.favouriteFilm)
    except Exception as e:
        flash('Failed to add to favourite ' + str(e))
        return render_template('dashboard.html', title='My Films', myFilms=user.favouriteFilm)
