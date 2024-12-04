# config.py
from dotenv import load_dotenv
import os

upload_folder = 'uploads/'
download_folder = 'downloads'
# 数据库路径
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_ID = '116122057'
    API_KEY = 'HxfskAbMtUeCRHKEuPk4Fvu0'
    SECRET_KEY = 'XdXaXciB6TWnqe5sRSrdxEvPodW5zszK'


def appconfig(env_path=None):
    load_dotenv(dotenv_path=env_path or '.env')
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(download_folder, exist_ok=True)


