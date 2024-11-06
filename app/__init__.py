# app/__init__.py
from flask import Flask
from app.config import appconfig
import os
from .fileops.fileops import fileops_bp
from .wenxin.route_openapi import openapi_bp

def create_app():
    app = Flask(__name__)

    # 配置环境变量
    appconfig()

    # 注册 Blueprint
    # 文心一言SDK
    # from .wenxin.route_sdk import chat_bp
    # app.register_blueprint(chat_bp)

    # 文心一言openapi

    app.register_blueprint(openapi_bp, url_prefix='/openapi')


    # 讯飞星火api
    # from .xinghuo.route_openapi import xinghuoapi_bp
    # app.register_blueprint(xinghuoapi_bp)

    #pdf文件操作

    app.register_blueprint(fileops_bp, url_prefix='/fileops')


    return app

