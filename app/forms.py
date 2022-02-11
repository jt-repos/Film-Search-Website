from flask_wtf import Form
from wtforms import IntegerField
from wtforms import TextField
from wtforms import DateTimeField
from wtforms import TimeField
from wtforms import DateField
from wtforms import PasswordField
from wtforms.validators import DataRequired

class RegisterForm(Form):
    username = TextField('username', validators=[DataRequired()])
    email = TextField('email', validators=[DataRequired()])
    password1 = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])

class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class ChangePasswordForm(Form):
    password = PasswordField('password', validators=[DataRequired()])
    password1 = PasswordField('password1', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])

class AddCinemaForm(Form):
    cinemaName = TextField('cinemaName', validators=[DataRequired()])
    address = TextField('address', validators=[DataRequired()])
    capacity = IntegerField('capacity', validators=[DataRequired()])
    openTime = TimeField('openTime', format='%H:%M:%S', validators=[DataRequired()])
    closeTime = TimeField('closeTime', format='%H:%M:%S', validators=[DataRequired()])

class AddFilmForm(Form):
    filmName = TextField('filmName', validators=[DataRequired()])
    length = IntegerField('length', validators=[DataRequired()])
    releaseDate = DateField('releaseDate', format='%d-%m-%Y', validators=[DataRequired()])
    studioName = TextField('studioName', validators=[DataRequired()])

class AddScreeningForm(Form):
    filmId = IntegerField('filmId', validators=[DataRequired()])
    cinemaId = IntegerField('cinemaId', validators=[DataRequired()])
