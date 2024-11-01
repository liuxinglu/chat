# app/__init__.py
from flask import Flask
from app.config import appconfig
import os


def create_app():
    app = Flask(__name__)

    # 配置环境变量
    appconfig(app)

    # 注册 Blueprint
    # 文心一言SDK
    # from .wenxin.route_sdk import chat_bp
    # app.register_blueprint(chat_bp)

    # 文心一言openapi
    # from .wenxin.route_openapi import openapi_bp
    # app.register_blueprint(openapi_bp)


    # 讯飞星火api
    # from .xinghuo.route_openapi import xinghuoapi_bp
    # app.register_blueprint(xinghuoapi_bp)

    #pdf文件操作
    from .fileops.fileops import fileops_bp
    app.register_blueprint(fileops_bp)


    return app

