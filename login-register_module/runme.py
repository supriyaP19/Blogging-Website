from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, Markup
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import func

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

@app.route('/dashboardComments')
def showcomments():
    userid_loggedin=flask_alchemytry.User.query.filter_by(user_name=session['username']).first()
    
    all_posts=flask_alchemytry.Posts.query.filter_by(post_userid=userid_loggedin.user_id).all()
    all_posts_comments=[]
    ucomment_details=[]
    acomment_details=[]
    titles=[]
    for i in all_posts:
        print("i: ",i)
        title=(i.post_title)
        titles.append(title)
        print("title: ",title)
        
        this_post_comments=flask_alchemytry.Comments.query.filter_by(comment_postid=i.post_id).all()
        print("This post comments; ",this_post_comments)
        all_posts_comments.append(this_post_comments)

        for j in this_post_comments:
            print("j: ",j)
            try:
                by=flask_alchemytry.User.query.filter_by(user_id=j.comment_userid).first()
                print("By: ",by)
                temp=[by.user_name,j.comment_content,title]
                ucomment_details.append(temp)
            except:
                temp=[j.comment_content,title]
                acomment_details.append(temp)

    # for i in range(total_posts_com):
    #     for j in range(len(all_posts_comments[i])):
    #         try:
    #             post=[]
    #             by=flask_alchemytry.User.query.filter_by(user_id=all_posts_comments[i][j].comment_userid).first()
    #             print("By: ",by)
    #             temp=[by.user_name,all_posts_comments[i][j].comment_content,title]
    #             comment_details.append(temp)
    #         except:
    #             temp=["Anonymous",all_posts_comments[i][j].comment_content,title]
    #             comment_details.append(temp)
    print("ULIST: ",ucomment_details," alist: ",acomment_details)
    return render_template('viewcomments.html',ulist=ucomment_details,alist=acomment_details)


@app.route('/themeChange/<int:tid>')
def themeChange(tid):
    theme = flask_alchemytry.User.query.filter_by(user_name=session['username']).first()
    theme.user_themeid=tid
    flask_alchemytry.db.session.add(theme)
    flask_alchemytry.db.session.commit()
    # flas.update().where(users.c.id==5).values(name="some name")
    return showPosts(session['username'])


def count(pid):
    connection = sqlite3.connect("blogger_db1.db")
    crsr = connection.cursor()
    # command="""select count(*) from comments where comment_postid=1"""
    crsr.execute("select count(*) from comments where comment_postid = %d"%pid)
    numberOfRows = crsr.fetchone()[0]
    connection.commit()
    connection.close()
    return numberOfRows

def count_posts(uid):
    connection = sqlite3.connect("blogger_db1.db")
    crsr = connection.cursor()
    # command="""select count(*) from comments where comment_postid=1"""
    crsr.execute("select count(*) from posts where post_userid = %d"%uid)
    numberOfRows = crsr.fetchone()[0]
    connection.commit()
    connection.close()
    return numberOfRows

def user_posts(uid):
    all_posts=flask_alchemytry.Posts.query.filter_by(post_userid=uid).all()
    for i in all_posts:
        comment_ids=flask_alchemytry.Comments.query.filter_by(comment_postid=i.post_id).all()
    return len(comment_ids)

def count_without_where():
    connection = sqlite3.connect("blogger_db1.db")
    crsr = connection.cursor()
    # command="""select count(*) from comments where comment_postid=1"""
    crsr.execute("select count(*) from posts")
    numberOfRows = crsr.fetchone()[0]
    connection.commit()
    connection.close()
    return numberOfRows

def findMonth(month):
    mon=[]
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
    return mon

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
        cid=0
        max_comment_id = db.session.query(func.max(flask_alchemytry.Comments.comment_id)).scalar()
        if max_comment_id:
            cid=max_comment_id+1
        else:
            cid=1
        try:
            userid=flask_alchemytry.User.query.filter_by(user_name=session['username']).first()
            
            new_com = flask_alchemytry.Comments(cid,id,userid.user_id,ts1,user_com)
            flask_alchemytry.db.session.add(new_com)
            flask_alchemytry.db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('showPosts',name=userid.user_name))
        except:
            new_com = flask_alchemytry.Comments(cid,id,-1,ts1,user_com)
            flask_alchemytry.db.session.add(new_com)
            flask_alchemytry.db.session.commit()
            return redirect(url_for('showmore',id=id))
        
    # return "RECORD ADDED"
# @app.route('/')
# def index():
#     return render_template("index.html")

# class LoginForm(Form):
#     username = StringField('Username', [validators.Length(min=4, max=25),validators.Required()])
#     password = PasswordField('Password')

@app.route('/showmore/<int:id>/', methods=['GET', 'POST'])
def showmore(id):
    comment_details=[]
    
    post_content=flask_alchemytry.Posts.query.filter_by(post_id=id)
    content = Markup(post_content[0].post_content)
    date = ((post_content[0].post_published_on).strftime('%m/%d/%Y %H:%M:%S')).split(" ")
    date_substring=(date[0]).split('/')
    mon=findMonth(date_substring[0])
    title=post_content[0].post_title
    id=post_content[0].post_id

    publisher=flask_alchemytry.User.query.filter_by(user_id=post_content[0].post_userid).first()
    print("content is  ***",post_content[0].post_content)
    
    post_details=[mon,date_substring[1],date_substring[2],title,content,id,publisher.user_name]

    all_comments=flask_alchemytry.Comments.query.filter_by(comment_postid=id).all()
    comm_content=[]
    for i in all_comments:
        comm_content.append(i.comment_content)

    print("Comments: ",comm_content)

    # print("Comments: ",comm_content)


    
    user_id=[]
    for i in all_comments:
         user_id.append(i.comment_userid)

    print("Commented users: ",user_id)
    
    names=[]
    for i in user_id:
        if i==-1:
            names.append("Anonymous")
        else:
            user_name_i=flask_alchemytry.User.query.filter_by(user_id=i).first()
            names.append(user_name_i.user_name)

    print("Commented user names:", names)
    

    for i,j in zip(comm_content,names):
        temp_det=[]
        temp_det.append(i)
        temp_det.append(j)
        comment_details.append(temp_det)


    print("COMMENT DET: ",comment_details)


    try:
        theme = flask_alchemytry.User.query.filter_by(user_name=session['username'])
        id = theme[0].user_themeid
        
        if id == "1":   
            return render_template('showmore.html',post_content=post_details,comments=comment_details)
        elif id == "2":
            return render_template('showmore_2.html',post_content=post_details,comments=comment_details)
        else:
            return render_template("viewPost2.html",num_com=n,pid=postid,post=temp,x=mon,time=time,day=day,year=year,uname=uname,post_title=title)
    except:
        return render_template('showmore.html',post_content=post_details,comments=comment_details)




@app.route('/showall/<string:name>/',methods=['GET','POST'])
def showPosts(name):
    print ("in SHOW POSTS")

    userid=flask_alchemytry.User.query.filter_by(user_name=uname).first()


    posts=flask_alchemytry.Posts.query.filter_by(post_userid=userid.user_id).all()
    print ("Posts: ",posts)

    # try:
    temp=[]
    time=[]
    mon=[]
    day=[]
    year=[]
    uname=[]
    title=[]
    postid=[]
    n=[]
    my_posts=count_posts(userid.user_id)
    my_comments=user_posts(userid.user_id)


        # posts=flask_alchemytry.Posts.query.all()
    try:
    # for i in posts:
    #     print(i.post_id)
    # print("inside showall",session['username']
        temp=[]
        time=[]
        mon=[]
        day=[]
        year=[]
        uname=[]
        title=[]
        postid=[]
        n=[]
    # print posts

        for i in posts:
            #find num of Comments
            # num=flask_alchemytry.Comments.query.filter_by(post_id=i.post_id).all()
            # n=session.query(Comments).filter(Comments.post_id.like(i.post_id)).count()
            num=count(i.post_id)
            n.append(num)
            str = i.post_content
            print("i=",i,"str: ",i.post_content)
            str = str[0:150]
            # print("date is: ",i.post_published_on)
            postid.append(i.post_id)
            date = ((i.post_published_on).strftime('%m/%d/%Y %H:%M:%S')).split(" ")
            print("date: ",date)
            date1 = (date[0]).split('/')
            # day=date1[0]
            month = date1[0]
            year.append(date1[2])
            day.append(date1[1])
            temp.append(Markup(str)) #has post content
            mon=findMonth(month)
            time.append(((date[1]).split(":"))[0] + ":" + ((date[1]).split(":"))[1])
            user = flask_alchemytry.User.query.filter_by(user_id=i.post_userid)
            title.append(i.post_title)
            uname.append(user[0].user_name)
        theme = flask_alchemytry.User.query.filter_by(user_name=session['username'])
        id = theme[0].user_themeid
        # print("the id is ",id)
        print("DATE: ",mon, time, day, year)
        if id == "1":   
            return render_template("viewPost.html",num_com=n,pid=postid,post=temp,x=mon,time=time,day=day,year=year,uname=uname,post_title=title,name=name)
        elif id == "2":
            colors=["card blue-grey darken-1","card blue darken-1","card green darken-1"]
           
            return render_template("viewPost1.html",colors=colors,num_com=n,pid=postid,post=temp,x=mon,time=time,day=day,year=year,uname=uname,post_title=title,name=name)
        elif id == "3":
            colors=["card blue-grey darken-1","card blue darken-1","card green darken-1"]
           
            return render_template("viewPost2.html",colors=colors,num_com=n,pid=postid,post=temp,x=mon,time=time,day=day,year=year,uname=uname,post_title=title,name=name)
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

@app.route('/blog_url',methods=['GET', 'POST'])
def blog_url():
    name = request.form['searchbar']
    print("inside blogurl",name)
    try:
        user = flask_alchemytry.User.query.filter_by(user_name=name)
        url = user[0].user_blog_url
        print("url is : ",url)
        return redirect(url)
        # return showPosts(name)
    except:
        return dashboard()

@app.route('/',methods=['GET','POST'])
def login():
    session['detect']=2
    if 'logged_in' in session:
            # uname = session['username']
            return redirect(url_for('dashboard'))
    else:
        num_posts=count_without_where()
        post_all = flask_alchemytry.Posts.query.all()
        print("Number of Posts: ",num_posts)
        index1=random.randint(0,int(num_posts/2))
        index2=random.randint(int(num_posts/2)+1,num_posts-1)
        print("index1: ",index1,"index2: ",index2)
        print("here i am")
        published_by=[]
        user_0=flask_alchemytry.User.query.filter_by(user_id=post_all[index1].post_userid).first()
        print ("user0 id; ",user_0)
        published_by.append(user_0.user_name)
        print ("P[0]: ",published_by)
        user_1=flask_alchemytry.User.query.filter_by(user_id=post_all[index2].post_userid).first()
        print ("user1 id; ",user_1)

        published_by.append(user_1.user_name)
        print ("P[1]: ",published_by)

        # form = LoginForm(request.form)
        post1 = flask_alchemytry.Posts.query.filter_by(post_id = post_all[index1].post_id).first()
        print("post1: ",post1)
        content1 =post1.post_content
        content1  = Markup(content1 [0:150])

        post2 = flask_alchemytry.Posts.query.filter_by(post_id = post_all[index2].post_id).first()
        print("post2: ",post2)
        content2 = post2.post_content
        # print "i=",i,"str: ",i.post_content
        content2 = Markup(content2 [0:150])
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
    return render_template("index.html",post1=post1,post2=post2,c1=content1,c2=content2,publishedBy=published_by)

@app.route('/detector_edit')
def detector_edit():
    print("inside detector edit")
    session['detect']=4
    print("value",session['detect'])
    return dashboard()
@app.route('/detector_add')
def detector_add():
    print("inside detector")
    session['detect']=5
    print("value",session['detect'])
    return dashboard()
@app.route('/detector_view')
def detector_view():
    print("inside detector")
    session['detect']=2
    print("value",session['detect'])
    return dashboard()
@app.route('/detector_publish')
def detector_publish():
    print("inside detector")
    session['detect']=1
    print("value",session['detect'])
    return dashboard()
@app.route('/detector_delete')
def detector_delete():
    print("inside detector")
    session['detect']=3
    print("value",session['detect'])
    return dashboard()

@app.route('/detect/<int:id>/',methods=['GET','POST'])
def detect_function(id):
    if session['detect']==1:
        print("inside publish")
    elif session['detect']==2:
        print("inside view")
        return showmore(id)
    elif session['detect']==3:
        print("inside delete")
        # postid = db.session.query(func.max(flask_alchemytry.User.user_id)).scalar()
        # d = flask_alchemytry.Posts.delete(flask_alchemytry.Posts.post_id==id)
        # d.execute()sk_sqlalchemy.BaseQuery' is not mapped
        post = flask_alchemytry.Posts.query.filter_by(post_id=id)
        flask_alchemytry.db.session.delete(post[0])
        flask_alchemytry.db.session.commit()
        session['detect']=2
        return dashboard()
    elif session['detect']==4:
        print("inside edit")
    elif session['detect']==5:
        print("inside add")
    return dashboard()

@app.route('/save',methods=['GET','POST'])
def save():
    # print("inside save")
    # return "OOPS"
    form = add_post_form(request.form)
    if request.method == 'POST':
        title = form.post_title.data
        content = form.post_content.data

        print(title)
        print(content)

        post_id = flask_alchemytry.Posts.query.all()
        post_index = post_id[len(post_id)-1]
        post_index = post_index.post_id + 1

        current_username = session['username']
        user_obj = flask_alchemytry.User.query.filter_by(user_name = current_username).first()
        userid_here = user_obj.user_id

        new_post = flask_alchemytry.Posts(int(post_index),int(userid_here),datetime.now(),content,title,'draft')
        flask_alchemytry.db.session.add(new_post)
        flask_alchemytry.db.session.commit()

    list_of_posts=[]
    user= flask_alchemytry.User.query.filter_by(user_name=session['username'])
    posts = flask_alchemytry.Posts.query.filter_by(post_userid=user[0].user_id)

    for i in posts:
        list_of_posts.append(i)

    return render_template('dashboard.html',username=session['username'],form=form,list_of_posts=list_of_posts)


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out!','success')
    return redirect(url_for('login'))


class add_post_form(Form):
    post_title = StringField('post_title',[validators.Required()])
    post_content = TextAreaField('post_content',[validators.Required()])

@app.route('/dashboard',methods=['GET','POST'])
@is_logged_in
def dashboard():
    form = add_post_form(request.form)
    if request.method == 'POST':
        title = form.post_title.data
        content = form.post_content.data
        print("wtfffffffffff")
        print(title)
        print(content)

        post_id = flask_alchemytry.Posts.query.all()
        post_index = post_id[len(post_id)-1]
        post_index = post_index.post_id + 1

        current_username = session['username']
        user_obj = flask_alchemytry.User.query.filter_by(user_name = current_username).first()
        userid_here = user_obj.user_id

        print("post_index-----------------:",post_index)
        print("userid-----------------:",userid_here)

        new_post = flask_alchemytry.Posts(int(post_index),int(userid_here),datetime.now(),content,title,'published')
        # new_post = flask_alchemytry.Posts(int(102),int(15),datetime.now(),'trying','hello')
        flask_alchemytry.db.session.add(new_post)
        flask_alchemytry.db.session.commit()


        # user_data = flask_alchemytry.User.query.all()
        # get_index = user_data[len(user_data)-1]
        # get_index = get_index.user_id + 1
        # new_user = flask_alchemytry.User(get_index,username,email,password,username+'.com','my blog',1)
        # flask_alchemytry.db.session.add(new_user)
        # flask_alchemytry.db.session.commit()
        

    list_of_posts=[]
    user= flask_alchemytry.User.query.filter_by(user_name=session['username'])
    posts = flask_alchemytry.Posts.query.filter_by(post_userid=user[0].user_id)

    for i in posts:
        list_of_posts.append(i)

    return render_template('dashboard.html',username=session['username'],form=form,list_of_posts=list_of_posts)





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
    num_posts=count_without_where()
    post_all = flask_alchemytry.Posts.query.all()
    print("Number of Posts: ",num_posts)
    index1=random.randint(0,int(num_posts/2))
    index2=random.randint(int(num_posts/2)+1,num_posts-1)
    print("index1: ",index1,"index2: ",index2)
    print("here i am")
    published_by=[]
    user_0=flask_alchemytry.User.query.filter_by(user_id=post_all[index1].post_userid).first()
    print ("user0 id; ",user_0)
    published_by.append(user_0.user_name)
    print ("P[0]: ",published_by)
    user_1=flask_alchemytry.User.query.filter_by(user_id=post_all[index2].post_userid).first()
    print ("user1 id; ",user_1)

    published_by.append(user_1.user_name)
    print ("P[1]: ",published_by)

    # form = LoginForm(request.form)
    post1 = flask_alchemytry.Posts.query.filter_by(post_id = post_all[index1].post_id).first()
    print("post1: ",post1)
    content1 =post1.post_content
    content1  = Markup(content1 [0:150])

    post2 = flask_alchemytry.Posts.query.filter_by(post_id = post_all[index2].post_id).first()
    print("post2: ",post2)
    content2 = post2.post_content
    # print "i=",i,"str: ",i.post_content
    content2 = Markup(content2 [0:150])
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        
        


        # user_data = flask_alchemytry.User.query.all()
        # get_index = user_data[len(user_data)-1]
        userid = db.session.query(func.max(flask_alchemytry.User.user_id)).scalar()
        session['detect']=2
        try:
            get_index = userid+1
            # get_index = get_index.user_id + 1
            new_user = flask_alchemytry.User(get_index,username,email,password,'http://127.0.0.1:5000/showall/'+username+'/',username+"'"+"s Blog",1)
            flask_alchemytry.db.session.add(new_user)
            flask_alchemytry.db.session.commit()


            flash('You are now registered and can log in', 'success')

            return redirect(url_for('login'))
        except:

            new_user = flask_alchemytry.User(1,username,email,password,'http://127.0.0.1:5000/showall/'+username+'/',username+"'"+"s Blog",1)
            flask_alchemytry.db.session.add(new_user)
            flask_alchemytry.db.session.commit()
            flash('You are now registered and can log in', 'success')

            return redirect(url_for('login'))

        return redirect(url_for('login'))
    return render_template('reg.html', form=form,post1=post1,post2=post2,c1=content1,c2=content2,publishedBy=published_by)
    

@app.route('/about')
def about():
    return render_template('about.html')

if(__name__) == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)