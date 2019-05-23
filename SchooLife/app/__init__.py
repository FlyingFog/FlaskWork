from flask import Flask
import config
import sqlite3
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(config.Config)


db = SQLAlchemy(app)


from .auth import auth as blueauth
app.register_blueprint(blueprint=blueauth)








