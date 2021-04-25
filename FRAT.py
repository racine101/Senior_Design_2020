import platform
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import sys
import mysql.connector 
import email_local

def clearAttendanceCSV():
    f = open('/home/frat/Documents/gitProjects/Senior_Design_2020/Attendance.csv','r+') 
    f.truncate(0)
    f.close()
def writeAttendanceCSV():
    f = open('/home/frat/Documents/gitProjects/Senior_Design_2020/Attendance.csv','r+') 
    f.writelines("Name,Time")

clearAttendanceCSV()
writeAttendanceCSV()

conn = mysql.connector.connect(user='frat' , password='ELEG4482', host='localhost' , database='Face_Recognition')

cursor = conn.cursor()

if conn.is_connected():
    print('Connected to MySQL database')

 
path = '/home/frat/Documents/gitProjects/Senior_Design_2020/testImages' 
images = []
classNames = []
myList = os.listdir(path)
nameList= []
print(  myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
 
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
    
# def markAttendanceCSV(name):
#     with open('/home/frat/Documents/gitProjects/Senior_Design_2020/Attendance.csv','r+') as f:
#         myDataList = f.readlines()
#         AttendanceList = []
#         for line in myDataList:
#             entry = line.split(',')
#             AttendanceList.append(entry[0])
#         if name not in nameList:
#             AttendanceList.append(name)
#             print( AttendanceList)
#             now = datetime.now()
#             dtString = now.strftime('%H:%M:%S')
#             f.writelines(f'\n{name},{dtString}')



def markAttendanceCSV(name):
    with open('/home/frat/Documents/gitProjects/Senior_Design_2020/Attendance.csv','r+') as f:
        myDataList = f.readlines()
        AttendanceList = []
        for line in myDataList:
            entry = line.split(',')
            AttendanceList.append(entry[0])
        if name not in AttendanceList:
            AttendanceList.append(name)
            # print( AttendanceList)
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

def showAttendance():
    cursor.execute("Select * from Attendance")
    result = cursor.fetchall()
    for x in result:
        print(x)


def markAttendance(name):
    now = datetime.now()
    dtString = now.strftime('%H:%M:%S')

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

def running_on_jetson_nano():
    # To make the same code work on a laptop or on a Jetson Nano, we'll detect when we are running on the Nano
    # so that we can access the camera correctly in that case.
    # On a normal Intel laptop, platform.machine() will be "x86_64" instead of "aarch64"
    return platform.machine() == "aarch64"
 

def get_jetson_gstreamer_source(capture_width=1280, capture_height=720, display_width=1280, display_height=720, framerate=60, flip_method=0):
    """
    Return an OpenCV-compatible video source description that uses gstreamer to capture video from the camera on a Jetson Nano
    """
    return (
            f'nvarguscamerasrc ! video/x-raw(memory:NVMM), ' +
            f'width=(int){capture_width}, height=(int){capture_height}, ' +
            f'format=(string)NV12, framerate=(fraction){framerate}/1 ! ' +
            f'nvvidconv flip-method={flip_method} ! ' +
            f'video/x-raw, width=(int){display_width}, height=(int){display_height}, format=(string)BGRx ! ' +
            'videoconvert ! video/x-raw, format=(string)BGR ! appsink'
            )
 
encodeListKnown = findEncodings(images)
print('Encoding Complete')

 
cap = cv2.VideoCapture(2)
 
while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
 
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
 
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        matchIndex = np.argmin(faceDis)
    
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
            markAttendanceCSV(name)
        else:
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
            cv2.putText(img,"Unknown",(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    
    


    imgr = cv2.resize(img, (940, 540))
    cv2.imshow('F.R.A.T',imgr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        showAttendance()
        clearAttendanceTable()
        email_local.send_Email()
        break
    

