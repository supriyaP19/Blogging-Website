from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, Markup
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy

from functools import wraps
import flask_alchemytry #import *
from functools import wraps
from datetime import datetime
import random
import sqlite3
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogger_db1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

#flask_alchemytry.db.create_all()

user = flask_alchemytry.User.query.all()
print(user)
keepme = True
def count(pid):
    connection = sqlite3.connect("blogger_db1.db")
    crsr = connection.cursor()
    # command="""select count(*) from comments where comment_postid=1"""
    crsr.execute("select count(*) from comments where comment_postid = %d"%pid)
    numberOfRows = crsr.fetchone()[0]
    connection.commit()
    connection.close()
    return numberOfRows

@app.route('/comment/<int:pid>')
def post_comment(pid):
    # if pid is None:
    #     return "OOPS"
    # else:
    #     # return "<h2 style=color:green>Hello %s !</h2>" % name
    return render_template("comment.html",pid=pid)

@app.route('/comment-result/<int:id>',methods=['POST', 'GET'])
def publish_comment(id):

    if request.method == 'POST':
        user_com = request.form['comment']
        ts1 = datetime.now()
        userid=flask_alchemytry.User.query.filter_by(user_name=session['username']).first()
        new_com = flask_alchemytry.Comments(random.randint(1,101),id,userid.user_id,ts1,user_com)
        flask_alchemytry.db.session.add(new_com)
        flask_alchemytry.db.session.commit()
        flash('Record was successfully added')
        return redirect(url_for('showPosts'))
    # return "RECORD ADDED"
# @app.route('/')
# def index():
#     return render_template("index.html")

# class LoginForm(Form):
#     username = StringField('Username', [validators.Length(min=4, max=25),validators.Required()])
#     password = PasswordField('Password')
@app.route('/fullBlog/<int:pid>')
def showMore(pid):
    # if pid is None:
    #     return "OOPS"
    # else:
    #     # return "<h2 style=color:green>Hello %s !</h2>" % name
    return render_template("comment.html",pid=pid)


@app.route('/showall',methods=['GET','POST'])
def showPosts():
    print "in SHOW POSTS"
    # theme = User.query.filter_by(user_name=)
    userid=flask_alchemytry.User.query.filter_by(user_name=session['username']).first()
    # <User 12>
    # a= str(s)
    # print a

    posts=flask_alchemytry.Posts.query.filter_by(post_userid=userid.user_id).all()
    print "Posts: ",posts


    # posts=flask_alchemytry.Posts.query.all()
    try:
    # for i in posts:
    #     print(i.post_id)
    # print("inside showall",session['username'])
        temp=[]
        time=[]
        mon=[]
        day=[]
        year=[]
        uname=[]
        title=[]
    # print posts

        for i in posts:
            #find num of Comments
            # num=flask_alchemytry.Comments.query.filter_by(post_id=i.post_id).all()
            # n=session.query(Comments).filter(Comments.post_id.like(i.post_id)).count()
            n=count(i.post_id)
            str = i.post_content
            print "i=",i,"str: ",i.post_content
            str = str[0:150]
            # print("date is: ",i.post_published_on)
            date = ((i.post_published_on).strftime('%m/%d/%Y %H:%M:%S')).split(" ")
            # print("secs :",date[1])
            date1 = (date[0]).split('/')
            month = date1[1]
            year.append(date1[2])
            day.append(date1[0])
            temp.append(Markup(str))
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
        theme = flask_alchemytry.User.query.filter_by(user_name=session['username'])
        id = theme[0].user_themeid
        # print("the id is ",id)

        if id == "1":
            return render_template("viewPost.html",num_com=n,post=temp,x=mon,time=time,day=day,year=year,uname=uname,post_title=title)
        elif id == "2":
            return render_template("viewPost1.html",num_com=n,post=temp,x=mon,time=time,day=day,year=year,uname=uname,post_title=title)
        else:
            return render_template("viewPost2.html",num_com=n,post=temp,x=mon,time=time,day=day,year=year,uname=uname,post_title=title)
    except:
        return render_template("no_posts.html")

#check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized','danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/',methods=['GET','POST'])
def login():
    if 'logged_in' in session:
            return redirect(url_for('dashboard'))
    else:
        print("here i am")
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
                if request.form.get('alive'):
                    session.permanent = True
                else:
                    session.permanent = False

                print("hey ",session['username'])
                flash('you are now logged in!!')


                return redirect(url_for('dashboard'))

            else:
                flash('Please enter valid username and password', 'failure')
    return render_template("index.html")




@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out!','success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')



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



if(__name__) == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
