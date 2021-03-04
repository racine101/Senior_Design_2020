import sys
import mysql.connector 
from datetime import datetime

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

# cursor.execute(""" SHOW TABLES""")
def showAttendance():
    cursor.execute("Select * from Attendance")
    result = cursor.fetchall()
    for x in result:
        print(x)

# data = cursor.fetchall()
# print(data)

def markAttendance(name):
    now = datetime.now()
    dtString = now.strftime('%H:%M:%S')

    nameList = []
    if name not in nameList:
        nameList.append(name)
        sql = "Insert INTO Attendance VALUES(%s,%s)"
        val = (name,dtString)
        cursor.execute(sql,val)
        conn.commit()

def clearAttendanceTable():
    sql= "DELETE FROM Attendance"
    cursor.execute(sql)
    conn.commit()

clearAttendanceTable()


conn.close()