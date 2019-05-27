import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "hahaha"
    #db Config

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask.db')
    #mysql://root:123456@localhost:3306/flask
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Mail Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '25'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "2420851839@qq.com"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "osoefenkedbneacj"
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <2420851839@qq.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or "2420851839@qq.com"
