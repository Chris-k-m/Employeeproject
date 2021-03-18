import mysql.connector

db = mysql.connector.connect(host="localhost",
                             user="root",
                             password="root",
                             database="online_ventures"
                             )
cursor = db.cursor()

# sqlform = "INSERT INTO employee (name, salary) VALUES(%s,%s)"

# employees = [("animsa", 70999), ("gerusi", 68900), ("bazuen", 90000), ]

# cursor.executemany(sqlform, employees)
# cursor.execute("ALTER TABLE employee ADD COLUMN designation CHAR(15) AFTER  id, ADD COLUMN department_name CHAR(100) NOT NULL,ADD COLUMN country CHAR(100) NOT NULL,ADD COLUMN gender CHAR(10) NOT NULL")
# cursor.execute("CREATE TABLE department( department_name CHAR(20), userid int, FOREIGN KEY (userid) REFERENCES employee(id))")
# cursor.execute("CREATE TABLE gender( male CHAR(10),userid int, FOREIGN KEY (userid) REFERENCES employee(id))")
# cursor.execute("CREATE TABLE country ( country_name CHAR (100), userid int, FOREIGN KEY (userid) REFERENCES employee(id))")
# cursor.execute("CREATE TABLE designation( location CHAR(100), userid int, FOREIGN KEY (userid) REFERENCES employee(id))")

# cursor.execute("CREATE TABLE password ( password VARCHAR (250), password_id int PRIMARY KEY AUTO_INCREMENT)")
# cursor.execute("ALTER TABLE password MODIFY password_id VARCHAR(250) AUTO_INCREMENT PRIMARY KEY")

# cursor.execute('drop table password')
cursor.execute('ALTER TABLE password ADD CONSTRAINT fk_password_emp FOREIGN KEY (employee_id) REFERENCES employee (employee_id)')











