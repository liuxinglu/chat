# config.py
from dotenv import load_dotenv
import os

upload_folder = 'uploads/'
download_folder = 'downloads'

def appconfig():
    load_dotenv()
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(download_folder, exist_ok=True)


