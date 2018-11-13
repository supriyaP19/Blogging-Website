from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, Markup
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from functools import wraps
import flask_alchemytry #import *


# app = Flask(__name__,static_url_path='/static')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogger_db1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

#flask_alchemytry.db.create_all()

user = flask_alchemytry.User.query.all()
print(user)



@app.route('/')
def index():
    return render_template("index.html")

# class LoginForm(Form):
#     username = StringField('Username', [validators.Length(min=4, max=25),validators.Required()])
#     password = PasswordField('Password')

@app.route('/showall',methods=['GET','POST'])
def showPosts():
    
    # theme = User.query.filter_by(user_name=)
    posts=flask_alchemytry.Posts.query.filter_by(post_userid=session['username'])

    for i in posts:
        print(i.post_id)
    # print("inside showall",session['username'])
    temp=[]
    time=[]
    mon=[]
    day=[]
    year=[]
    uname=[]
    title=[]
    postid=[]
    for i in posts:
        str = i.post_content
        str = Markup(str)
        str = str[0:200]
        # print("date is: ",i.post_published_on)
        date = ((i.post_published_on).strftime('%m/%d/%Y %H:%M:%S')).split(" ")
        print("secs :",date[1])
        date1 = (date[0]).split('/')
        month = date1[1]
        year.append(date1[2])
        day.append(date1[0])
        temp.append(str)
        if month=="1" or month=="01":
            mon.append("January")
        elif month=="2" or month=="02":
            mon.append("February")
        elif month=="3" or month=="03":
            mon.append("March")
        elif month=="4" or month=="04":
            mon.append("April")
        elif month=="5" or month=="05":
            mon.append("May")
        elif month=="6" or month=="06":
            mon.append("June")
        elif month=="7" or month=="07":
            mon.append("July")
        elif month=="8" or month=="08":
            mon.append("August")
        elif month=="9" or month=="09":
            mon.append("September")
        elif month=="10":
            mon.append("October")
        elif month=="11":
            mon.append("November")
        elif month=="12":
            mon.append("December")
        time.append(((date[1]).split(":"))[0] + ":" + ((date[1]).split(":"))[1])
        user = flask_alchemytry.User.query.filter_by(user_id=i.post_userid)
        title.append(i.post_title)
        uname.append(user[0].user_name)
        postid.append(i.post_id)
    theme = flask_alchemytry.User.query.filter_by(user_name=session['username'])
    id = theme[0].user_themeid
    name = theme[0].user_name
    # print("the id is ",id)

    if id == "1":
        return render_template("viewPost.html",post=temp,x=mon,time=time,day=day,year=year,uname=uname,post_title=title,pid=postid,name=name)
    elif id == "2":
        return render_template("viewPost1.html",post=temp,x=mon,time=time,day=day,year=year,uname=uname,post_title=title,pid=postid,name=name)
    else:
        return render_template("viewPost2.html",post=temp,x=mon,time=time,day=day,year=year,uname=uname,post_title=title,pid=postid,name=name)

@app.route('/blog_url',methods=['GET', 'POST'])
def blog_url():
    name = request.form['searchbar']
    # print("inside blogurl",name)
    user = flask_alchemytry.User.query.filter_by(user_name=session['username'])
    url = user[0].user_blog_url
    return render_template(url)

@app.route('/showmore/<int:id>/', methods=['GET', 'POST'])
def showmore(id):
    post_content = flask_alchemytry.Posts.query.filter_by(post_id=id)

    print("content is  *****",post_content[0].post_content)
    content = Markup(post_content[0].post_content)

    return render_template('showmore.html',post_content=content)


@app.route('/comment-result/<int:id>/', methods=['GET', 'POST'])
def comment(id):
    print("the id is: ",id)
    current_user = flask_alchemytry.User.query.filter_by(user_name=session['username'])
    userid = current_user[0].user_id
    # print(" user idis -=============",userid)
    max_comment_id = db.session.query(func.max(flask_alchemytry.Comments.comment_id)).scalar()
    if max_comment_id:
        print("yes")
    else:
        print("no")
   
    return render_template('showmore.html',id=id)

@app.route('/login',methods=['GET','POST'])
def login():
    print("here")
    # form = LoginForm(request.form)

    print(request.method)
    if request.method == 'POST':
        username = request.form['username']

        password = request.form['user_password']
   
        check_user = flask_alchemytry.User.query.filter_by(user_name = username).first()
        print("post")
        if check_user and sha256_crypt.verify(password, check_user.user_password):
            session['logged_in']=True
            session['username']=username
            flash('you are now logged in!!')

            # print("hey t=rajjo",session['username'])
            return render_template('dashboard.html')
        	
        else:
            flash('Please enter valid username and password', 'failure')
            return render_template("index.html")

# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50),validators.Required()])
    username = StringField('Username', [validators.Length(min=4, max=25),validators.Required()])
    email = StringField('Email', [validators.Length(min=6, max=50),validators.Required()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/reg', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))



        user_data = flask_alchemytry.User.query.all()
        get_index = user_data[len(user_data)-1]
        get_index = get_index.user_id + 1
        new_user = flask_alchemytry.User(get_index,username,email,password,username+'.com','my blog',1) 
        flask_alchemytry.db.session.add(new_user)
        flask_alchemytry.db.session.commit()
		

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('reg.html', form=form)




# @app.route('/reg')
# def reg():
#     return render_template("reg.html")




# @app.route('/login')
# def login():
#     form = LoginForm(request.form)
#     if request.method == 'POST' and form.validate():
#         username = form.username.data
#         # email = form.email.data
#         # username = form.username.data
#         password = sha256_crypt.encrypt(str(form.user_password.data))

#         check_user = User.query.filter_by(user_name = username, user_password = password)

#         if check_user:
#         	return render_template('login.html', form = form)
        	
#         else:
#         	flash('Please enter valid username and password', 'failure')

#     return render_template('reg.html', form = form)


if(__name__) == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
    