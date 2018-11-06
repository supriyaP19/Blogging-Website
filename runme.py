from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",login = True )

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

        # # Create cursor
        # cur = mysql.connection.cursor()

        # # Execute query
        # cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # # Commit to DB
        # mysql.connection.commit()

        # # Close connection
        # cur.close()

        flash('You are now registered and can log in', 'success')

        # return redirect(url_for('login'))
    return render_template('reg.html', form=form)



# @app.route('/reg')
# def reg():
#     return render_template("reg.html")

@app.route('/login')
def login():
    return render_template("login.html")
if(__name__) == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
    