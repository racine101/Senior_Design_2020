import sys
import mysql.connector 

conn = mysql.connector.connect(user='frat' , password='ELEG4482', host='localhost' , database='Face_Recognition')

cursor = conn.cursor()

if conn.is_connected():
    print('Connected to MySQL database')

# sql = "INSERT INTO Student VALUES(%s,%s,%s,%s,%s)"
# val = ("21322860","Ty","Jone","M", "Senior")

# # cursor.execute(sql,val)

# conn.commit()
# data = cursor.fetchall()
# print(data)

cursor.execute(""" SHOW TABLES""")

cursor.execute("Select * from Student")
result = cursor.fetchall()
for x in result:
    print(x)

data = cursor.fetchall()
print(data)


conn.close()