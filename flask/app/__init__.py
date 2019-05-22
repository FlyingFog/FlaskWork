from flask import Flask
import config
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from .views import blue

app = Flask(__name__)
app.config.from_object(config.Config)

db = SQLAlchemy(app)

app.register_blueprint(blueprint=blue)









