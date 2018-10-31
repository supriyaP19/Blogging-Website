from flask import Flask
from flask import session
from flask import render_template
from flask import request
import models as dbHandler

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

###################### root ##################################################
@app.route('/')
def index():
   if 'username' in session:
      return render_template("index.html", logged_in = True,  username=session['username'])
   else:
      return render_template("index.html", logged_in = False,  username=None)

 
####################### login #################################################
@app.route('/login', methods=['POST', 'GET'])
def login():
   if 'username' in session:
        return render_template("result.html", message=session['username'] +" has already logged in,  first logout!!!")
   elif request.method == 'POST':
        if dbHandler.authenticate(request): 
            session['username'] = request.form['username']
            msg = "successful login" 
        else: 
           msg ="login failed"

	return render_template("result.html", message=msg)
                                                            
   
   return render_template('login.html')

######################## logout #################################################
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'username' in session:
        name = session.pop('username')
        return render_template("result.html", message=name +" has logged out Successfully.")
    
    return render_template("result.html", message="You are already logged out.")

######################### register ################################################
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
	if not dbHandler.checkBlogUrl(request) :
	    msg = "Blog Url taken. Please enter unique url!!"
        elif dbHandler.insertUser(request) :
            msg = "success in adding user"
        else:
            msg = "failed to add existing user"

	return render_template("result.html", message=msg)
    
    return render_template('register.html')

######################################################################### 
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')

