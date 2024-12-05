from flask import Blueprint, render_template, redirect, url_for, flash, session, current_app
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from app.database import db
from app.model.models import User
from .forms import RegistrationForm
from .forms import LoginForm
from io import BytesIO
from app.tool.base_tool import generate_captcha
from app.services import user_service

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_service.create_user(form.username.data, form.password.data)
        flash('注册成功！请登录。', category='success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = user_service.authenticate_user(form.username.data, form.password.data, form.captcha.data)
        if user:
            login_user(user)
            session['user_id'] = user.id
            flash('登录成功！', category='success')
            return redirect(url_for('index'))
        else:
            flash('用户名、密码或验证码无效', category='error')
            return redirect(url_for('auth.login'))
    captcha_image, _ = generate_captcha()
    return render_template('auth/login.html', form=form, captcha_image=captcha_image)


@auth_bp.route('/captcha')
def captcha():
    image, captcha_text = generate_captcha()
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = current_app.response_class(response=buf_str, status=200, mimetype='image/jpeg')
    return response


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功！', category='success')
    return redirect(url_for('auth.login'))
