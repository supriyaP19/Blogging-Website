from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogger_db1.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column('user_id',db.Integer,primary_key=True,unique=True)
    user_name=db.Column('user_name',db.Unicode,nullable=False)
    user_email=db.Column('user_email',db.Unicode,nullable=False,unique=True)
    user_password=db.Column('user_password',db.Unicode,nullable=False)
    user_blog_url=db.Column('user_blog_url',db.Unicode,unique=True)
    user_blog_title=db.Column('user_blog_title',db.Unicode)
    user_themeid=db.Column('user_themeid',db.Unicode, db.ForeignKey('theme.theme_id', onupdate='CASCADE', ondelete='RESTRICT'))
    posts =db.relationship('Posts',backref='owner')

    def __init__(self,id,name,email,password,blog_url,blog_title,themeid):
        self.user_id = id
        self.user_name = name
        self.user_email = email
        self.user_password = password
        self.user_blog_url = blog_url
        self.user_blog_title = blog_title
        self.user_themeid = themeid
    
class Posts(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column('post_id',db.Integer,primary_key = True,unique=True,nullable=False)
    post_userid = db.Column('post_userid',db.Integer, db.ForeignKey('user.user_id', onupdate='CASCADE', ondelete = 'CASCADE'),nullable=False)
    post_published_on = db.Column('post_published_on',db.DateTime,default = datetime.utcnow)
    post_content = db.Column('post_content',db.Unicode)
    post_title = db.Column('post_title',db.Unicode)
#    __table_args__ = (ForeignKeyConstraint(onupdate = 'CASCADE', ondelete = 'CASCADE') )

    def __init__(self, id, userid,published_on, content, title):
        self.post_id = id
        self.userid = userid
        self.published_on = published_on
        self.post_content = content
        self.post_title = title     

class Theme(db.Model):
    __tablename__ = 'theme'
    theme_id = db.Column('theme_id', db.Integer,primary_key=True)

    def __init__(self,id):
        self.theme_id = id
        

class Comments(db.Model):
    comment_id = db.Column('comment_id',db.Integer,nullable=False,primary_key=True)
    comment_postid = db.Column('comment_postid',db.Integer, db.ForeignKey('posts.post_id', onupdate='cascade', ondelete = 'cascade'),nullable=False)
    comment_userid = db.Column('comment_userid',db.Integer, db.ForeignKey('user.user_id', onupdate='cascade', ondelete = 'cascade'), nullable=False)
    comment_date = db.Column('comment_date',db.DateTime, default = datetime.utcnow)
    comment_content = db.Column('comment_content',db.Unicode,nullable=False)

    def __init__(self, id, postid, userid, date, content):
        self.comment_id = id
        self.comment_postid = postid
        self.comment_userid = userid
        self.comment_date = date
        self.comment_content = content

class Follows(db.Model):
    #table_id = db.Column()
    #follows_id_auto = db.Column('follows_id',db.Integer, primary_key=True)
    follows_id = db.Column('follows_id', db.ForeignKey('user.user_id', ondelete = 'cascade', onupdate = 'cascade'), nullable=False,primary_key=True)
    follows_userid = db.Column('follows_userid', db.ForeignKey('user.user_id', ondelete = 'cascade', onupdate = 'cascade'), nullable=False,primary_key=True)

    def __init__(self, followsid, followsuserid):
        self.follows_id = followsid
        self.follows_userid = followsuserid
   
   
class Followers(db.Model):
    #table_id = db.Column()
   #followers_id_auto = db.Column('followers_id',db.Integer, primary_key=True)
    followers_id = db.Column('followers_id', db.ForeignKey('user.user_id', ondelete = 'cascade', onupdate = 'cascade'), nullable=False, primary_key=True)
    followers_userid = db.Column('followers_userid', db.ForeignKey('user.user_id', ondelete = 'cascade', onupdate = 'cascade'), nullable=False, primary_key=True)

    def __init__(self, followersid, followersuserid):
        self.followers_id = followersid
        self.followers_userid = followersuserid
