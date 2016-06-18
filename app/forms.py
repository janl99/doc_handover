from flask.ext.wtf import Form
from wtforms import TextField,BooleanField,StringField,TextAreaField
from wtforms.validators import Required,Email,Length

class LoginForm(Form):
    username = TextField('username',validators = [Required()])
    password = TextField('password',validators = [Required()])

class UserEditForm(Form):
    username = StringField('username', [Required()])
    email = TextField('email', [Required(),Email()])
    about_me = TextAreaField('about me', [Length(min=6,max=256)])
    dynamic = TextField('dynamic',[Length(min=6,max=64)])
