
from flask import current_app, render_template, redirect, request, url_for, flash
from flask_login import login_user as flask_login_user
from flask_login import logout_user, login_required, current_user, fresh_login_required

from . import auth
from .forms import *

from .. import db
from ..models import User


@auth.route('/login/user', methods=['GET', 'POST'])
def login_user():
    # 如果已經登入了 還打這網址 就直接導回首頁
    if current_user.is_active:
        return redirect(url_for('main.index'))
    # 如果沒有登入
    form = LoginForm()
    # 如果validate成功
    if form.validate_on_submit():
        # 在資料庫裡查詢那個user
        user = User.query.filter_by(email=form.email.data).first()
        # 如果有查到email而且password hash對的話
        if user is not None and user.verify_password(form.password.data):
            # 如果有勾記住我, 就直接記住你
            flask_login_user(user, remember=form.remember_me.data)
            # flash一個message, 丟進隊伍, base.html加入相對應get_flash_message
            flash(u'成功登入')
            # 如果成功登入就導到首頁
            return redirect(url_for('main.index'))
        # user沒查到或者密碼部正確
        flash(u'不存在的帳號名稱或密碼不正確')
    # 沒成功回去login.html
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # 創造這個form
    form = RegistrationForm()
    # 執行form裡面這個函式
    if form.validate_on_submit():
        # 加入資料庫
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # 導回去叫他登入
        return redirect(url_for('auth.login_user'))
    # 如果validate不通過, 才會再次register
    return render_template('auth/register.html', form=form)












