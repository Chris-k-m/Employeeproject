import re

import MySQLdb.cursors
import mysql.connector
from flask import Flask, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash

app = Flask(__name__)
Bootstrap(app)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

mysql = MySQL()

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'online_ventures'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/online_ventures/login', methods=['GET', 'POST'])
def login():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # check if data is in db
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE email = %s AND password =MD5(%s)', (email, password))
        # Fetch one record and return result
        employee = cursor.fetchone()
        # if account exists
        if employee:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['employee_id'] = employee['employee_id']
            session['user_name'] = employee['user_name']
            # Redirect to home page
            return render_template("home.html")
        else:
            # employee doesnt exist or username/password incorrect
            msg = 'Incorrect email/password!'
            # Show the login form with message (if any)
            return render_template('login.html', msg=msg)
    return render_template('login.html', )


@app.route('/online_ventures/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # validate the received values
    if request.method == 'POST' and "user_name" in request.form and "sir_name" in request.form and "gender" in request.form and "password" in request.form and "password2" in request.form and "email" in request.form:
        user_name = request.form['user_name']
        sir_name = request.form['sir_name']
        gender = request.form['gender']
        password = request.form['password']
        password2 = request.form['password2']
        email = request.form['email']
        DOB = request.form["DOB"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE user_name = %s', (user_name,))
        employee = cursor.fetchone()
        # If account exists show error and validation checks
        if employee:
            'employee already exists!'
            return render_template('register.html')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return render_template("register.html", msg="email has a match")
        elif not re.match(r'[A-Za-z0-9]+', user_name):
            return render_template("register.html", msg="only use letters and No's")
        if password != password2:
            return render_template("register.html", msg="password don't match")
        elif not user_name or not password or not email:
            msg = 'Please refill out the form!'
            return render_template("home.html", msg=msg)

        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Account doesnt exists and the form data is valid, now insert new account into employee table
            cursor.execute('INSERT INTO employee VALUES (NULL, %s, %s, %s, MD5(%s), %s, %s, NULL, NULL,NULL)',
                           (user_name, sir_name, email, password, gender, DOB))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
        return render_template('login.html', msg='You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

    # do not save password as a plain text


# # Output message if something goes wrong...
# msg = ''
# # Check if "username", "password" and "email" POST requests exist (user submitted form)
# if request.method == 'POST' and 'user_name' in request.form and 'password' in request.form and 'email' in request.form:
#     # Create variables for easy access
#     user_name = request.form['user_name']
#     password = request.form['password']
#     password2 = request.form['password2']
#     email = request.form['email']
#     # Check if account exists using MySQL
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute('SELECT * FROM employee WHERE user_name = %s', (user_name,))
#     employee = cursor.fetchone()
#     # If account exists show error and validation checks
#     if employee:
#         msg = 'employee already exists!'
#     elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#         return render_template("register.html", message="email has a match")
#     elif not re.match(r'[A-Za-z0-9]+', user_name):
#         return render_template("register.html", message="only use letters and numbers")
#     if password != password2:
#         return render_template("register.html", message="password don't match")
#     elif not user_name or not password or not email:
#         msg = 'Please fill out the form!'
#     else:
#         # Account doesnt exists and the form data is valid, now insert new account into accounts table
#         cursor.execute('INSERT INTO employee VALUES (NULL, %s , %s, %s)', (user_name, password, email,))
#         mysql.connection.commit()
#         msg = 'You have successfully registered!'
# elif request.method == 'POST':
#     # Form is empty... (no POST data)
#     msg = 'form empty!'
# # Show registration form with message (if any)
# return render_template('register.html', msg=msg)


@app.route("/online_ventures/details")
def details():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE employee_id = % s', (session['employee_id'],))
        employee = cursor.fetchone()
        return render_template("details.html", employee=employee)
    return render_template("login.html")


@app.route('/onlineventures/logout')
def logout():
    # check if user is logged in:
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('employee_id', None)
    session.pop('user_name', None)
    # Redirect to login page
    return render_template("login.html")


@app.route('/onlineventures/home')
def home():
    # Check if employee is loggedin
    if 'loggedin' in session:
        # employee is loggedin show them the home page
        return render_template('home.html', user_name=session['user_name'])
    # User is not loggedin redirect to login page
    return render_template("login.html")


@app.route('/online_ventures/add_details', methods=['GET', 'POST'])
def add_details():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'email' in request.form and 'departmentid' in request.form and 'countryid' in request.form and 'designationid' in request.form:
            email = request.form['email']
            departmentid = request.form['departmentid']
            countryid = request.form['countryid']
            designationid = request.form['designationid']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM employee WHERE email = % s', (email,))
            employee = cursor.fetchone()
            if employee:
                cursor.execute(
                    'UPDATE employee SET email =% s, departmentid =% s, countryid =% s, designationid =% s WHERE employee_id =% s',
                    (email, departmentid, countryid, designationid, (session['employee_id']),))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
                print(email, departmentid, departmentid, countryid)
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("add_details.html", msg=msg)
    return render_template("login.html")

    # if request.method == 'POST' and 'countryid' in request.form and 'departmentid' in request.form and 'designatonid' in request.form:
    #     countryid = request.form['countryid']
    #     designationid = request.form['designationid']
    #     departmentid = request.form['departmentid']
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     employee = cursor.fetchone()
    #     cursor.execute = (
    #             "UPDATE employee SET departmentid = %s,countryid = %s, designationid = %s WHERE employee_id = employee_id)",
    #             (departmentid, countryid, designationid))
    #     mysql.connection.commit()
    #     msg = "update done successfully"
    #     return render_template("details.html", msg=msg, employee=employee)
    # else:
    #     msg = "update error"
    #     return render_template("add_details.html", msg=msg)


@app.route('/onlineventures/department')
def department():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute = ('SELECT * FROM department')
    department = cursor.fetchall()
    return render_template("department.html", department=department)


@app.route('/onlineventures/country')
def country():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute = ('SELECT * FROM country')
    country = cursor.fetchall()
    return render_template("country.html", country=country)


@app.route('/onlineventures/designation')
def designation():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute = ('SELECT * FROM designation')
    designation = cursor.fetchall()
    return render_template("designation.html", designation=designation)


@app.route('/online_ventures/delete')
def delete_user():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM employee WHERE employee_id=%s", (session['employee_id']))
    mysql.connection.commit()
    msg = 'User deleted successfully!'
    return render_template('/', msg=msg)


@app.route('/online_ventures/add_department', methods=['GET', 'POST'])
def add_department():
    # Output message if something goes wrong...
    msg = ''
    # validate the received values
    if request.method == 'POST' and "departmentid" in request.form and "department_name" in request.form:
        departmentid = request.form['departmentid']
        department_name = request.form['department_name']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM department WHERE departmentid = %s', (departmentid,))
        department = cursor.fetchone()
        if department:
            msg = 'department exists'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Account doesnt exists and the form data is valid, now insert new account into employee table
            cursor.execute('INSERT INTO department VALUES (%s, %s)',
                           (departmentid, department_name))
            mysql.connection.commit()
            msg = 'You have successfully added departments!'
        return render_template('department.html', msg=msg)
    return render_template("department.html")


@app.route('/online_ventures/add_designation', methods=['GET', 'POST'])
def add_designation():
    # Output message if something goes wrong...
    msg = ''
    # validate the received values
    if request.method == 'POST' and "designationid" in request.form and "designation_name" in request.form:
        designationid = request.form['designationid']
        designation_name = request.form['designation_name']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM designation WHERE designationid = %s', (designationid,))
        designation = cursor.fetchone()
        if designation:
            msg = 'designation exists'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Account doesnt exists and the form data is valid, now insert new account into employee table
            cursor.execute('INSERT INTO designation VALUES (%s, %s)',
                           (designationid, designation_name))
            mysql.connection.commit()
            msg = 'You have successfully added departments!'
        return render_template('designation.html', msg=msg)
    return render_template("designation.html")


@app.route('/online_ventures/add_country', methods=['GET', 'POST'])
def add_country():
    # Output message if something goes wrong...
    msg = ''
    # validate the received values
    if request.method == 'POST' and "countryid" in request.form and "country_name" in request.form:
        countryid = request.form['countryid']
        country_name = request.form['country_name']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM country WHERE countryid = %s', (countryid,))
        country = cursor.fetchone()
        if country:
            msg = 'country exists'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Account doesnt exists and the form data is valid, now insert new account into employee table
            cursor.execute('INSERT INTO country VALUES (%s, %s)',
                           (countryid, country_name))
            mysql.connection.commit()
            msg = 'You have successfully added country!'
        return render_template('country.html', msg=msg)
    return render_template("country.html")


@app.errorhandler(404)
def page_not_found(e):
    return "page not found", 404


@app.errorhandler(500)
def internal_error(e):
    return "internal error", 500

# if __name__ == "__main__":
#     app.run(debug=True)
