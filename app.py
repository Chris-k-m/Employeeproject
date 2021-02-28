from flask_mysqldb import MySQL
import pymysql
import MySQLdb.cursors
import re
from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
Bootstrap(app)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

mysql = MySQL()

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'onlineventures'

mysql.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/onlineventures/login', methods=['GET', 'POST'])
def login():
    # connect
    # Output message if something goes wrong...
    msg = ''
    #     # 1. grab data from form
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # check if data is in db
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE email = %s AND password = %s', (email, password))
        # Fetch one record and return result
        employee = cursor.fetchone()
        # if account exists
        if employee:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = employee['id']
            session['first_name'] = employee['first_name']
            # Redirect to home page
            return render_template("home.html")
        else:
            # employee doesnt exist or username/password incorrect
            msg = 'Incorrect email/password!'
    # Show the login form with message (if any)
    return render_template('index.html')


@app.route('/onlineventures/details')
def details():
    # check if account exists using MYSQL
    conn = mysql.connect
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM employee WHERE id = %s', (session['id'],))
        employee = cursor.fetchone()
        # Show the profile page with account info
        return render_template('details.html', employee=employee)
    # User is not loggedin redirect to login page
    return render_template("login.html")


@app.route('/onlineventures/logout')
def logout():
    # check if user is logged in:

    # if 'loggedin' in session:
    # check if user is logged in:
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('first_name', None)
    # Redirect to login page
    return render_template("login.html")


@app.route('/onlineventures/home')
def home():
    # Check if employee is loggedin
    if 'loggedin' in session:
        # employee is loggedin show them the home page
        return render_template('home.html', first_name=session['first_name'])
    # User is not loggedin redirect to login page
    return render_template("login.html")


@app.errorhandler(404)
def page_not_found(e):
    return "page not found", 404


@app.errorhandler(500)
def internal_error(e):
    return "internal error", 500


# if __name__ == "__main__":
#      app.run(debug=True)
