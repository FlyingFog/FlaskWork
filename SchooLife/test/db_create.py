from app import db

from app import models
from urllib import parse
session = db.session

models.dropDB()
models.creatDB()