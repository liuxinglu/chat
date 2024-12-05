from app.database import db
from app.model.models import User
from flask import session

# 创建用户
def create_user(username, password):
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

# 认证用户
def authenticate_user(username, password, captcha):
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return None
    if captcha.lower() != session.get('captcha', ''):
        return None
    return user