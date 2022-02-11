import os
import unittest
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models, views

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_redirects(self):
        response = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/create', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/changePassword', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/addFilm', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/addCinema', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/addScreening', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/markAsFavourite/0', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_insert_film(self):
        response = views.getFilmRow("film1", 100, "12-10-2019", "studio1")
        self.assertEqual(response.filmName, "film1")
        self.assertEqual(response.releaseDate, "12-10-2019")

    def test_insert_film_edge(self):
        filmName = ""
        for i in range(0, 128):
            filmName += "a"
        response = views.getFilmRow(filmName, 1, "01-01-1900", "a")
        self.assertEqual(response.filmName, filmName)
        self.assertEqual(response.releaseDate, "01-01-1900")
        self.assertEqual(response.studioName, "a")

    def test_insert_film_invalid1(self):
        filmName = ""
        response = views.getFilmRow(filmName, 1, "01-01-1900", "a")
        self.assertEqual(response, -1)

    def test_insert_film_invalid2(self):
        filmName = ""
        for i in range(0, 129):
            filmName += "a"
        response = views.getFilmRow(filmName, 1, "01-01-1900", "a")
        self.assertEqual(response, -1)

    def test_insert_film_invalid3(self):
        response = views.getFilmRow("film2", 0, "01-01-1900", "a")
        self.assertEqual(response, -1)

    def test_insert_film_invalid4(self):
        date = datetime.date(1990, 10, 10)
        response = views.getFilmRow("film2", 100, date, "")
        self.assertEqual(response, -1)

    def test_insert_cinema(self):
        openTime = datetime.time(12, 0, 0)
        closeTime = datetime.time(19, 0, 0)
        response = views.getCinemaRow("name", "address", 100, openTime, closeTime)
        self.assertEqual(response.cinemaName, "name")
        self.assertEqual(response.address, "address")
        self.assertEqual(response.capacity, 100)
        self.assertEqual(response.openTime, openTime)
        self.assertEqual(response.closeTime, closeTime)

    def test_insert_cinema_edge(self):
        cinemaName = ""
        for i in range(0, 128):
            cinemaName += "a"
        openTime = datetime.time(12, 0, 0)
        closeTime = datetime.time(19, 0, 0)
        response = views.getCinemaRow(cinemaName, "a", 1, openTime, closeTime)
        self.assertEqual(response.cinemaName, cinemaName)
        self.assertEqual(response.address, "a")
        self.assertEqual(response.capacity, 1)

    def test_insert_cinema_invalid1(self):
        cinemaName = ""
        openTime = datetime.time(12, 0, 0)
        closeTime = datetime.time(19, 0, 0)
        response = views.getCinemaRow(cinemaName, "a", 1, openTime, closeTime)
        self.assertEqual(response, -1)

    def test_insert_cinema_invalid2(self):
        cinemaName = ""
        for i in range(0, 129):
            cinemaName += "a"
        openTime = datetime.time(12, 0, 0)
        closeTime = datetime.time(19, 0, 0)
        response = views.getCinemaRow(cinemaName, "a", 1, openTime, closeTime)
        self.assertEqual(response, -1)

    def test_insert_cinema_invalid3(self):
        response = views.getCinemaRow("cinema", "a", 0, "aaaa", "bbb")
        self.assertEqual(response, -1)

    def test_insert_cinema_invalid4(self):
        openTime = datetime.time(12, 0, 0)
        closeTime = datetime.time(19, 0, 0)
        response = views.getCinemaRow("cinema", "a", -100, openTime, closeTime)
        self.assertEqual(response, -1)

    def test_user(self):
        response = views.getUserRow("user", "email", "password")
        self.assertEqual(response.username, "user")
        self.assertEqual(response.email, "email")
        self.assertEqual(response.password, "password")

    def test_user_edge(self):
        password = ""
        for i in range(0, 32):
            password += "a"
        response = views.getUserRow("1", "1", password)
        self.assertEqual(response.username, "1")
        self.assertEqual(response.email, "1")
        self.assertEqual(response.password, password)

    def test_user_invalid1(self):
        password = ""
        for i in range(0, 33):
            password += "a"
        response = views.getUserRow("1", "1", password)
        self.assertEqual(response, -1)

    def test_user_invalid1(self):
        password = ""
        for i in range(0, 32):
            password += "a"
        response = views.getUserRow("", "", password)
        self.assertEqual(response, -1)

    def test_get_cinema(self):
        openTime = datetime.time(12, 0, 0)
        closeTime = datetime.time(19, 0, 0)
        p = models.Cinema(cinemaName="test",
    					address="address",
    					capacity=100,
    					openTime=openTime,
    					closeTime=closeTime)
        db.session.add(p)
        db.session.commit()
        cinema = models.Cinema.query.get(1)
        self.assertEqual(cinema.cinemaName, "test")
        self.assertEqual(cinema.address, "address")
        self.assertEqual(cinema.capacity, 100)
        self.assertEqual(cinema.openTime, openTime)
        self.assertEqual(cinema.closeTime, closeTime)

    def test_get_film(self):
        releaseDate = datetime.date(2000, 1, 1)
        p = models.Film(filmName="film",
                        length=100,
                        releaseDate=releaseDate,
                        studioName="name")
        db.session.add(p)
        db.session.commit()
        film = models.Film.query.get(1)
        self.assertEqual(film.filmName, "film")
        self.assertEqual(film.length, 100)
        self.assertEqual(film.releaseDate, releaseDate)
        self.assertEqual(film.studioName, "name")

    def test_get_user(self):
        p = models.User(username="test",email="email",password="pass")
        db.session.add(p)
        db.session.commit()
        user = models.User.query.get(1)
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "email")
        self.assertEqual(user.password, "pass")

if __name__ == '__main__':
    unittest.main()
