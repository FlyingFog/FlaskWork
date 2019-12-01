from flask import Flask
from flask_avatars import Avatars
from flask_bootstrap import Bootstrap
import config
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager


bootstrap = Bootstrap()

app = Flask(__name__)
app.config.from_object(config.Config)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'



db = SQLAlchemy()
mail = Mail()
avatars=Avatars()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    avatars.init_app(app)
    from .admin import admin
    admin.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    # '/'根路由是用auth注册的，自动打开的是根路由'/'
    # 使用前缀/auth后，登陆界面需要加个/auth才是对的，否则是not found
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(auth_blueprint)
    return app


