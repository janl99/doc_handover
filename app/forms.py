# -*- code:utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField,BooleanField,StringField,TextAreaField,PasswordField,FileField
from wtforms.validators import Required,Email,Length,EqualTo

class LoginForm(Form):
    username = TextField('username',validators = [Required()])
    password = TextField('password',validators = [Required()])

class UserEditForm(Form):
    email = TextField('email', [Required(),Email()])
    about_me = TextAreaField('about me', [Length(min=6,max=256)])
    dynamic = TextField('dynamic',[Length(min=6,max=64)])

class ChangePasswordForm(Form):
    password = PasswordField('password',validators=[Required()])
    newpassword = PasswordField('newpassword',validators=[Required(),Length(min=6,max=12)])
    confimpassword = PasswordField('confimpassword',validators=[Required(),Length(min=6,max=12),EqualTo('newpassword',message='password must be same.')])

class HeadimgForm(Form):
    headimg = TextField('headimg',validators=[Required()])
