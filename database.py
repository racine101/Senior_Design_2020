import sys
import mysql.connector 

conn = mysql.connector.connect(user='frat' , password='ELEG4482', host='localhost' , database='Face_Recognition')

cursor = conn.cursor()

if conn.is_connected():
    print('Connected to MySQL database')

cursor.execute(""" SHOW TABLES""")

data = cursor.fetchall()
print(data)


conn.close()