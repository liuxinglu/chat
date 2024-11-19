# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from app.config import appconfig
import logging
import os
from app.model.models import User
from app.database import db
from flask_migrate import Migrate


migrate = Migrate()


login_manager = LoginManager()
def create_app():
    app = Flask(__name__)

    # 配置环境变量
    appconfig()
    app.config.from_object('app.config.Config')

    # 初始化数据库和迁移
    db.init_app(app)
    migrate.init_app(app, db)

    app.secret_key = os.urandom(24).hex()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # 设置日志记录
    if not app.debug:
        file_handler = logging.FileHandler('error.log')
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

    # 注册 Blueprint
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    # 文心一言SDK
    # from .wenxin.route_sdk import chat_bp
    # app.register_blueprint(chat_bp)

    # 文心一言openapi
    from .wenxin.route_openapi import openapi_bp
    app.register_blueprint(openapi_bp, url_prefix='/wenxin')


    # 讯飞星火api
    from .xinghuo.route_openapi import xinghuoapi_bp
    app.register_blueprint(xinghuoapi_bp, url_prefix='/xinghuo')

    #pdf文件操作
    from .fileops.fileops import fileops_bp
    app.register_blueprint(fileops_bp, url_prefix='/fileops')

    # 页面操作
    from .control.routes import pageops_bp
    app.register_blueprint(pageops_bp, url_prefix='/pageops')


    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


