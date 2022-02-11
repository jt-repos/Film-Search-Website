from app import db
from flask_login import UserMixin, login_user, login_manager, login_required, logout_user, current_user

screening = db.Table('screening',
    db.Column('cinemaId', db.Integer, db.ForeignKey('cinema.cinemaId')),
    db.Column('filmId', db.Integer, db.ForeignKey('film.filmId')))

favouriteFilm = db.Table('favouriteFilm',
    db.Column('id', db.Integer, db.ForeignKey('user.id')),
    db.Column('filmId', db.Integer, db.ForeignKey('film.filmId')))

class Cinema(db.Model):
    cinemaId = db.Column(db.Integer, primary_key=True)
    cinemaName = db.Column(db.String(128))
    capacity = db.Column(db.Integer)
    openTime = db.Column(db.Time)
    closeTime = db.Column(db.Time)
    address = db.Column(db.String(256))
    screening = db.relationship('Film', secondary=screening, backref=db.backref('cinemaScreening', lazy='dynamic'))

class Film(db.Model):
    filmId = db.Column(db.Integer, primary_key=True)
    filmName = db.Column(db.String(128))
    length = db.Column(db.Integer)
    releaseDate = db.Column(db.Date)
    studioName = db.Column(db.String(128))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(32))
    password = db.Column(db.String(32), nullable=False)
    favouriteFilm = db.relationship('Film', secondary=favouriteFilm, backref=db.backref('favouriteFilm', lazy='dynamic'))
