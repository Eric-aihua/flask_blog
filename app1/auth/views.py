# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user
from flask_login import login_required, logout_user, current_user

from app1.decorators import admin_required, permission_required
from app1.email import send_email
from .. import db
from .forms import LoginForm, RegistrationForm
from ..models import User, Permission

from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                # 引用其他蓝本的url时，需要加上蓝本的名称
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

# 处理来自邮件的确认请求
# TODO
# 由于itsdangerous库生成token时存在问题，且暂时先不管邮箱的功能
# 先通过http://localhost:5000/auth/confirm/:id/的形式，手动在浏览器确认
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


# 为了保护路由只让认证用户访问， Flask-Login 提供了一个 login_required 修饰器,如果未认证的用户访问这个路由， Flask-Login 会拦截请求，把用户发往登录页面
@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

# 演示只有通过admin的觉得才能访问
@auth.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

# 演示只有MODERATE_COMMENTS权限的用户才能访问
@auth.route('/moderator')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment moderators!"


# app的request的拦截
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))



@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))