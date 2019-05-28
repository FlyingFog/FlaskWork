from flask import Flask
import config
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

mail = Mail()
app = Flask(__name__)
app.config.from_object(config.Config)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

db = SQLAlchemy(app)
mail.init_app(app)
login_manager.init_app(app)

from .auth import auth as blueauth
app.register_blueprint(blueprint=blueauth)








