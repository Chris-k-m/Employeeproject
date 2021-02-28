import mysql.connector

db = mysql.connector.connect(host="localhost",
                             user="root",
                             password="root",
                             database="onlineventures"
                             )
cursor = db.cursor()

# employee_details = "INSERT INTO employee (first_name, sir_name, email, phone, password) VALUES " + ", ".join(["(%s, %s, %s, %s,%s )"])
# employees = [
#     (" Michael", "Skepta", "michaelsk@gmail.com", "0744563720", "root"),
#     (" Brian", "Bricks", "Bbricks@gmail.com", "0744563722", "1234"),
#     (" chris", "kysta", "ckysta@gmail.com", "77899543", "freshi")
#        ]
