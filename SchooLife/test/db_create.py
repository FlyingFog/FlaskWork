from app import db

from app import models

session = db.session

models.dropDB()
models.creatDB()