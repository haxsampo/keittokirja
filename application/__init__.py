from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

import os
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///keittokirja.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app, session_options={"autoflush": False})

from application import views

from application.reseptit import models
from application.reseptit import views

from application.auth import models
from application.auth import views

from application.ohje import models

from application.ainesosat import models

from application.resepti_ainesosat import models

from application.misc.sqlhelp import startupInsertionContainer

#user authentication
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Tervetuloa "

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

try:
    db.create_all()
    startupInsertionContainer.insert_test_accounts()
except:
    pass


    
