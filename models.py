import sqlite3 as sql
from flask import session

def insertUser(request):
    con = sql.connect("BloggerDB.db")

    
    
    sqlQuery = "select username from user where (username ='" + request.form['usernamesp'] + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    print request.form['name']
    if not row:
        cur.execute("INSERT INTO user (name,gender,password,username,email,urlblog,urltitle) VALUES (?,?,?,?,?,?,?)", (request.form['name'],request.form['gender'],request.form['password'],request.form['usernamesp'],request.form['email'],request.form['urlblog'],request.form['urltitle']))
        con.commit()
        print "added user successfully"
       
    con.close()
    return not row

def checkBlogUrl(request):
    con = sql.connect("BloggerDB.db")
    sqlBlogUrl = "select username from user where (urlblog ='" + request.form['urlblog']+"')"
    cur = con.cursor()
    cur.execute(sqlBlogUrl)
    row = cur.fetchone()
    if row:
	print "This Blog Url is not available"
    con.close()
    return not row
    
    



def authenticate(request):
    con = sql.connect("BloggerDB.db")
   
    sqlQuery = "select username from users where (username ='" + request.form['username'] + "' and password ='" + request.form['password'] + "')"
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    con.close()
    return row
  
