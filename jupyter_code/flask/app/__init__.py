
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

from flask_admin import Admin
# 套件創造起來 -> 連結你的app
bootstrap = Bootstrap()
db = SQLAlchemy()
adm = Admin(name='Programmer')
# Login Manager會幫你處理所有Login的選項
login_manager = LoginManager()
login_manager.session_protection = 'strong'
# 如果有login_required, 沒登入就會幫你導回auth blueprint的login_user函式
login_manager.login_view = 'auth.login_user'
login_manager.login_message = u'請先登入您的帳號'


def create_app(config_name):
    app = Flask(__name__)
    # 套件跟app連結: 套件.init_app(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    # 自動幫你所有在blueprint的url前面加上/auth
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .test import test as test_blueprint
    app.register_blueprint(test_blueprint, url_prefix="/test")

    from .admin import AdminView, create_admin_view
    create_admin_view(adm, db)
    adm.init_app(app)

    return app

