import re
import MySQLdb.cursors
import mysql.connector
from flask import Flask, render_template, request, session
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
app.config['MYSQL_CURSOR_CLASS'] = 'DictCursor'

mysql.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/online_ventures/login', methods=['GET', 'POST'])
def login():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        # check if data is in db
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT password FROM password WHERE password =MD5(%s) ', (session['password'],))
        cursor.execute('SELECT * FROM employee WHERE email = %s ', (session['email'],))
        # Fetch one record and return result
        employee = cursor.fetchone()
        # if account exists
        if employee:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['employee_id'] = employee['employee_id']
            session['countryid'] = employee['countryid']
            session['departmentid'] = employee['departmentid']
            session['designationid'] = employee['designationid']
            session['user_name'] = employee['user_name']
            session['DOB'] = employee['DOB']
            session['sir_name'] = employee['sir_name']

            # Redirect to home page
            return render_template("home.html")
        else:
            # employee doesnt exist or username/password incorrect
            msg = 'Incorrect email/password!'
            # Show the login form with message (if any)
            return render_template('login.html', msg=msg)
    return render_template('login.html')


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
            cursor.execute('INSERT INTO employee VALUES (NULL, %s, %s, %s, %s, %s, NULL, NULL, NULL)',
                           (user_name, sir_name, email, gender, DOB,))
            cursor.execute('INSERT INTO password VALUES( MD5(%s), NULL,NULL)', (password,))
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
        cursor.execute('SELECT * FROM employee WHERE employee_id = %s', (session['employee_id'],))
        employee = cursor.fetchone()
        return render_template("details.html", employee=employee)
    return render_template("details.html")


@app.route('/onlineventures/home')
def home():
    # Check if employee is loggedin
    if 'loggedin' in session:
        # employee is loggedin show them the home page
        return render_template('home.html', user_name=(session['user_name']))
    # User is not loggedin redirect to login page
    return render_template("login.html")


@app.route('/online_ventures/add_details', methods=['GET', 'POST'])
def add_details():
    if 'loggedin' in session:
        # fetch data from database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM department')
        departments = cursor.fetchall()
        cursor.execute('SELECT * FROM country')
        countries = cursor.fetchall()
        cursor.execute('SELECT * FROM designation')
        designations = cursor.fetchall()
        if request.form == 'POST' and 'countryid' in request.form.get and 'departmentid' in request.form.get and 'designationid' in request.form.get:
            countryid = request.form.get['countryid']
            departmentid = request.get['departmentid']
            designationid = request.form.get['designationid']
            cursor.execute('UPDATE employee set countryid=%s, departmentid=%s, designationid=%s WHERE employee_id=%s',
                           (countryid, departmentid, designationid, (session['employee_id'],)))
            return render_template("add_details.html", msg='details saved')
        else:
            msg = 'details not yet saved'
        return render_template("add_details.html", msg=msg, countries=countries, designations=designations,
                               departments=departments)
    else:
        msg = 'details not filled'
    return render_template("add_details.html", msg=msg)


# if 'logged_in' in session:
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute('SELECT * FROM employee WHERE employee_id = % s', (session['employee_id'],))
#     cursor.execute('SELECT departmentid, department_name FROM department')
#     cursor.execute('SELECT countryid, country_name FROM country')
#     cursor.execute('SELECT designationid, designation_name FROM designation')
#     departments = cursor.fetchall()
#     countries = cursor.fetchall()
#     designations = cursor.fetchall()
#     employee = cursor.fetchone()
#     cursor.execute(
#                 'UPDATE employee SET departmentid =% s, countryid =% s, designationid =% s WHERE employee_id =% s',
#                 (departmentid, countryid, designationid, (session['employee_id']),))
#             mysql.connection.commit()
#             msg = 'You have successfully updated !'
#             return render_template("add_details.html", msg=msg, departments=departments, designations=designations,
#                                    countries=countries)
#     elif request.method == 'POST':
#         msg = 'Please fill out the form !'
#         return render_template("add_details.html", msg=msg)

# if request.method == 'POST' and 'countryid' in request.form and 'departmentid' in request.form and 'designatonid' in request.form:
#     countryid = request.form['countryid']
#     designationid = request.form['designationid']
#     departmentid = request.form['departmentid']
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     employee = cursor.fetchone()
#     cursor.execute = (f
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
    cursor.execute("select * FROM department")
    departments = cursor.fetchall()  # data from database
    return render_template("department.html", departments=departments)


@app.route('/onlineventures/country')
def country():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * FROM country")
    countries = cursor.fetchall()  # data from database
    return render_template("country.html", countries=countries)


@app.route('/onlineventures/designation')
def designation():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * FROM designation")
    designations = cursor.fetchall()  # data from database
    return render_template("designation.html", designations=designations)


@app.route('/online_ventures/delete')
def delete_user():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DROP * FROM employee WHERE employee_id=%s", (session['employee_id'],))
        mysql.connection.commit()
        msg = 'User deleted successfully!'
        return render_template('register.html', msg=msg)


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
    return render_template("add_department.html")


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
            cursor.execute('INSERT INTO designation VALUES (%s, %s)',
                           (designationid, designation_name))
            mysql.connection.commit()
            msg = 'You have successfully added departments!'
        return render_template('designation.html', msg=msg)
    return render_template("add_designation.html")


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
    return render_template("add_country.html")


@app.route('/online_ventures/edit_department', methods=['GET', 'POST'])
def edit_department():
    # validate if user has input data
    if request.method == 'POST' and "departmentid" in request.form and "department_name" in request.form:
        new_departmentid = request.form['departmentid']
        new_department_name = request.form['department_name']
        # connect to mysql database
        if 'loggedin' in session:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT departmentid FROM employee WHERE employee_id= %s', (session['employee_id'],))
            departmentid = cursor.fetchone()
            print(departmentid)
            print(new_departmentid)
            if departmentid != new_departmentid:
                cursor.execute('UPDATE department SET department_name = %s WHERE departmentid = %s',
                               (new_department_name, (session['departmentid'],)))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
                return render_template("department.html", msg=msg)
            else:
                msg = 'use the correct ID'
            return render_template("edit_department.html", msg=msg)
    else:
        msg = 'input data!'
        return render_template("edit_department.html", msg=msg)


@app.route('/online_ventures/edit_designation', methods=['GET', 'POST'])
def edit_designation():
    # validate if user has input data
    if request.method == 'POST' and "designationid" in request.form and "designation_name" in request.form:
        new_designationid = request.form['designationid']
        new_designation_name = request.form['designation_name']
        # connect to mysql database
        if 'loggedin' in session:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT designationid FROM employee WHERE employee_id= %s', (session['employee_id'],))
            designationid = cursor.fetchone()
            print(designationid)
            print(new_designationid)
            if designationid != new_designationid:
                cursor.execute('UPDATE designation SET designation_name = %s WHERE designationid = %s',
                               (new_designation_name, (session['designationid'],)))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
                return render_template("designation.html", msg=msg)
            else:
                msg = 'use the correct ID'
            return render_template("edit_designation.html", msg=msg)
    else:
        msg = 'input data!'
        return render_template("edit_designation.html", msg=msg)


@app.route('/online_ventures/edit_country', methods=['GET', 'POST'])
def edit_country():
    # validate if user has input data
    if request.method == 'POST' and "countryid" in request.form and "country_name" in request.form:
        new_countryid = request.form['countryid']
        new_country_name = request.form['country_name']
        # connect to mysql database
        if 'loggedin' in session:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT countryid FROM employee WHERE employee_id= %s', (session['employee_id'],))
            countryid = cursor.fetchone()
            print(countryid)
            print(new_countryid)
            if countryid != new_countryid:
                cursor.execute('UPDATE country SET country_name = %s WHERE countryid = %s',
                               (new_country_name, (session['countryid'],)))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
                return render_template("country.html", msg=msg)
            else:
                msg = 'use the correct ID'
            return render_template("edit_country.html", msg=msg)
    else:
        msg = 'input data!'
        return render_template("edit_country.html", msg=msg)


#     if 'loggedin' in session:
#         if request.method == 'POST' in request.form and "updatedcid" in request.form and "updatedcname" in request.form:
#             newcountryname= request.form['updatedcname']
#             newcountryid = request.form['updatedcid']
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cursor.execute("SELECT * FROM country WHERE countryid = %s", (session['countryid']))
#             cursor.execute("SELECT * FROM employee where employeeid = %s", (session['employeeid']))
#             employee = cursor.fetchone()  # data from database
#             if employee:
#                 cursor.execute('UPDATE country SET countryid = %s, country_name =%s, WHERE employee_id =% s',
#                                (newcountryid, newcountryname, (session['employeeid'])))
#                 mysql.connection.commit()
#                 msg = 'You have successfully added country!'
#                 return render_template('country.html', msg=msg)
#         msg = 'You havent added country yet!'
#     return render_template("edit_country.html", msg=msg)


@app.route('/onlineventures/logout')
def logout():
    # check if user is logged in:
    if 'loggedin' in session:
        # Remove session data, this will log the user out
        session.pop('loggedin', None)
        session.pop('employee_id', None)
        session.pop('user_name', None)
        session.clear()
        # Redirect to login page
    return render_template("login.html")


@app.errorhandler(404)
def page_not_found(e):
    return "page not found", 404


@app.errorhandler(500)
def internal_error(e):
    return "internal error", 500


if __name__ == "__main__":
    app.run(debug=True)
