from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from app.database import db

pageops_bp = Blueprint('pageops', __name__)



@pageops_bp.route('/getKeywordPage', methods=['GET'])
def getKeywordPage():
    return render_template('index.html')

@pageops_bp.route('/getBankPage', methods=['GET'])
def getBankPage():
    return render_template('bank.html')
