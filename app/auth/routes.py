from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from app import db
from app.model.models import User
from .forms import RegistrationForm
from .forms import LoginForm

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！请登录。', category='success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码无效', category='error')
            return redirect(url_for('auth.login'))
        login_user(user)
        flash('登录成功！', category='success')
        return redirect(url_for('index'))
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功！', category='success')
    return redirect(url_for('auth.login'))
