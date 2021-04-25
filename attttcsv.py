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