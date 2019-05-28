import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or "hahaha"
    #db Config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask.db')
    #mysql://root:123456@localhost:3306/flask
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #login Config

    #Mail Config
    """
    MAIL_SERVER = 'smtp.263.net'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@avery.com>'
    FLASKY_ADMIN = "flasktest"
    """
