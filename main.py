from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'super_secret_key'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Thds@19xcNh#20J'
app.config['MYSQL_DB'] = 'webdesign_lab3'

mysql = MySQL(app)
  
# @app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_records WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['userid'] = account['userid']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET','POST'])
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'phoneno' in request.form :
        username = request.form['username']
        password = request.form['password']
        phoneno = request.form['phoneno']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_records WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not phoneno:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user_records VALUES (NULL, % s, % s, % s)', (username, password, phoneno, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('registration.html', msg = msg)

@app.route('/courses')
def courses():
    return render_template('courses.html')
@app.route('/home')
def home():
    return render_template('home.html')
    
if __name__ == "__main__":
    app.run(debug=True)