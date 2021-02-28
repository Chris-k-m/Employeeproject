import mysql.connector

db = mysql.connector.connect(host="localhost",
                             user="root",
                             password="root",
                             database="onlineventures"
                             )
cursor = db.cursor()

# sqlform = "INSERT INTO employee (name, salary) VALUES(%s,%s)"

# employees = [("animsa", 70999), ("gerusi", 68900), ("bazuen", 90000), ]

# cursor.executemany(sqlform, employees)
# cursor.execute("ALTER TABLE employee ADD COLUMN designation CHAR(15) AFTER  id, ADD COLUMN department_name CHAR(100) NOT NULL,ADD COLUMN country CHAR(100) NOT NULL,ADD COLUMN gender CHAR(10) NOT NULL")
cursor.execute("CREATE TABLE department( department_name CHAR(20), userid int, FOREIGN KEY (userid) REFERENCES employee(id))")
# cursor.execute("CREATE TABLE gender( male CHAR(10),userid int, FOREIGN KEY (userid) REFERENCES employee(id))")
# cursor.execute("CREATE TABLE country ( country_name CHAR (100), userid int, FOREIGN KEY (userid) REFERENCES employee(id))")
# cursor.execute("CREATE TABLE designation( location CHAR(100), userid int, FOREIGN KEY (userid) REFERENCES employee(id))")
# cursor.execute("ALTER TABLE employee DROP COLUMN username")












