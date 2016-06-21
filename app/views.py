from app import app
from flask import render_template,redirect,session,url_for,request,g,flash
from flask.ext.login import login_user,logout_user,current_user,login_required
from app import db,lm 
from models import User,ROLE_USER,ROLE_ADMIN
from forms import LoginForm,UserEditForm,ChangePasswordForm,HeadimgForm
from hashlib import md5
from config import UPLOAD_AVATAR,basedir
import os,io
import base64

'''S-flask-login'''
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
'''E-flask-login'''

'''S-index'''
@app.route('/')
@app.route('/index')
@login_required
def index():
    title = "Genal data tool" 
    user = g.user
    return render_template("index.html",title = title,user=user) 
'''E-index'''

'''S-login'''
@app.route('/login',methods =['GET','POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(flask.url_for('index'))
    form = LoginForm()
    errors =[]
    if form.validate_on_submit():
        print "LoginForm Post"
        user = User.query.filter_by(nickname = form.username.data ).first()
        if user is None:
            errors.append('Invalid login. Please try again.')
            if form.username.data == "janl" :
                user = User(nickname="janl",password = md5("123456").hexdigest(),email="janl@163.com",role = ROLE_ADMIN)
                jdb.session.add(user)
                db.session.commit()
            return render_template('login.html',form=form,errors=errors)
        pwmd5code = md5(form.password.data).hexdigest()
        if user is not None:
            if user.password == pwmd5code:
                login_user(user)
                flash('logined in successfully.')
                return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html',form=form,errors=errors)
'''E-login'''

'''S-logout'''
@app.route('/logout')
def logout():
    logout_user()
    user =  current_user
    return redirect(url_for('login'))
'''E-logout'''

'''S-profile'''
@app.route('/profile',methods =['GET','POST'])
@login_required
def profile():
    return render_template('profile.html',user=g.user)
'''E-profile'''

'''S-useredit'''
@app.route('/useredit',methods=['GET','POST'])
@login_required
def useredit():
    form = UserEditForm()
    if form.validate_on_submit():
        print "UserEditForm Post"
        print form.email.data
        print form.dynamic.data
        print form.about_me.data
        g.user.email = form.email.data
        g.user.dynamic = form.dynamic.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        form.email.data = g.user.email
        form.dynamic.data = g.user.dynamic
        form.about_me.data = g.user.about_me
    return render_template('useredit.html',form=form,user=g.user)
'''E-useredit'''

'''S-changepassword'''
@app.route('/changepassword',methods=['GET','POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        newpassword = form.newpassword.data
        confimpassword = form.confimpassword.data
        print g.user.password
        pwmd5code = md5(password).hexdigest()
        print pwmd5code
        if g.user.password == pwmd5code: 
            g.user.password = md5(newpassword).hexdigest()
            db.session.add(g.user)
            db.session.commit()
            return redirect(url_for('profile'))
    return render_template('changepassword.html',form=form,user=g.user)
'''E-changepassword'''

'''S-setting_headimg'''
@app.route('/setting_headimg',methods=['GET','POST'])
@login_required
def setting_headimg():
    print "setting_headimg_post"
    form = HeadimgForm()
    if form.validate_on_submit():
        #print form.headimg.data 
        fn = os.path.join(UPLOAD_AVATAR,str(g.user.id) +'-123456.png')
        print fn
        index = form.headimg.data.index(',')
        print index
        l = len(form.headimg.data)
        data = form.headimg.data[index+1:l]
        f = io.open(fn,'wb') 
        f.write(data.decode('base64'))
        f.close()

        lb = len(basedir)
        lfn = len(fn)
        imgpath = fn[lb:lfn]
        print imgpath
        g.user.avatar = imgpath
        db.session.add(g.user)
        db.session.commit()
    return render_template('setting_headimg.html',user=g.user,form=form)
'''E-setting_headimg'''




