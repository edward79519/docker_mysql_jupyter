
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField(u'電子郵件',
                        validators=[DataRequired(message=u'請輸入電子郵件'), Length(1, 64, u'電子郵件超過長度'), Email(u'電子郵件不符合規範')])
    password = PasswordField(u'密碼', validators=[DataRequired(u'請輸入密碼')])
    remember_me = BooleanField(u'保持登入')
    submit = SubmitField(u'登入')


class RegistrationForm(Form):
    email = StringField(u'電子郵件', validators=[DataRequired(message=u'此欄位不得為空'), Length(1, 64), Email(u'電子郵件不符合規範')])
    username = StringField(u'使用者名稱', validators=[DataRequired(message=u'此欄位不得為空'), Length(1, 64),
                                                 Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'使用者名稱只允許使用英文.數字.小數點或者下底線')])
    password = PasswordField(u'密碼',
                             validators=[DataRequired(message=u'此欄位不得為空'), EqualTo('password2', message=u'密碼兩次必須輸入相同')])
    password2 = PasswordField(u'確認密碼', validators=[DataRequired(message=u'此欄位不得為空')])
    submit = SubmitField(u'註冊')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'電子郵件已註冊過')
