from flask import Flask
from flask_mail import Mail
import config
from flask_sqlalchemy import SQLAlchemy

mail = Mail()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    mail.init_app(app)
    db.init_app(app)

    # if app.config['SSL_REDIRECT']:
    #     from flask_sslify import SSLify
    #     sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    # '/'根路由是用auth注册的，自动打开的是根路由'/'
    # 使用前缀/auth后，登陆界面需要加个/auth才是对的，否则是not found
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(auth_blueprint)

    return app
