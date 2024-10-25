# app/__init__.py
from flask import Flask
from config import load_dotenv


def create_app():
    app = Flask(__name__)

    # 配置环境变量
    load_dotenv()

    # 注册 Blueprint
    # from .wenxin.route_sdk import chat_bp
    # app.register_blueprint(chat_bp)

    from .wenxin.route_openapi import openapi_bp
    app.register_blueprint(openapi_bp)


    return app
