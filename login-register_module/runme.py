from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import flask_alchemytry #import *


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
    posts=flask_alchemytry.Posts.query.all()
    for i in posts:
        print(i.post_id)
    # print("inside showall",session['username'])
    theme = flask_alchemytry.User.query.filter_by(user_name=session['username'])
    id = theme[0].user_themeid
    print("the id is ",id)

    # if id == 1:
    #     return render_template("viewPost.html",post=posts)
    # elif id == 2:
    #     return render_template("viewPost1.html",post=posts)
    # else:
    return render_template("viewPost.html",post=posts)


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

            print("hey t=rajjo",session['username'])
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
    