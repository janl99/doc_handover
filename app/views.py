from app import app
from flask import render_template,redirect,session,url_for,request,g,flash
from flask.ext.login import login_user,logout_user,current_user,login_required
from app import db,lm 
from models import User,ROLE_USER,ROLE_ADMIN
from forms import LoginForm,UserEditForm

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    title = "Genal data tool" 
    user = g.user
    return render_template("index.html",title = title,user=user) 

@app.route('/login',methods =['GET','POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(flask.url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname = form.username.data ).first()
        if user is None and form.user.data == "janl" :
            user = User(nickname="janl",password = "123456",email="janl@163.com",role = ROLE_ADMIN)
            db.session.add(user)
            db.session.commit()
            return render_template('login.html')
        if user is not None:
            if user.password == form.password.data:
                login_user(user)
                flash('logined in successfully.')
                return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    user =  current_user
    return redirect(url_for('login'))

@app.route('/profile',methods =['GET','POST'])
@login_required
def profile():
    userform = UserEditForm()
    print userform
    if userform.validate_on_submit():
        print userform.email.data
        print userform.dynamic.data
        print userform.about_me.data
        g.user.email = userform.email.data
        g.user.dynamic = userform.dynamic.data
        g.user.about_me = userform.about_me.data
        db.session.add(g.user)
        db.session.commit()
    return render_template('profile.html',user=g.user,userform=userform)
