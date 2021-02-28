import mysql.connector

db = mysql.connector.connect(host="localhost",
                             user="root",
                             password="",
                             database="onlineventures"
                             )
cursor = db.cursor()

cursor.execute("CREATE DATABASE onlineventures ")



