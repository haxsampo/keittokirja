from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
# Kolme vinoviivaa kertoo, tiedosto sijaitsee
# tämän sovelluksen tiedostojen kanssa samassa paikassa
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///keittokirja.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import views
from application.reseptit import models

db.create_all()