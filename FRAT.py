import platform
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

 
path = 'C:/VS_Code/Senior_Design/testImages'
images = []
classNames = []
#get a list of files in directory and  store it in the array 
myList = os.listdir(path)
print(myList)

#reading each image using the cv2 imread function
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    #getting the name of each file and only keeping the part before the .jpg
    classNames.append(os.path.splitext(cl)[0])
 

#finding the encodings and storing them in a array 
def findEncodings(images):
    encodeList = []
    for img in images:
        #convert the image to RGB 
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #find the encodings 
        encode = face_recognition.face_encodings(img)[0]
        #appending the encoding to a array
        encodeList.append(encode)
    return encodeList



    
def markAttendance(name):
    with open('C:/VS_Code/Senior_Design/Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

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


            

#Calling the Find encoding function 
encodeListKnown = findEncodings(images)
print('Encoding Complete')

#getting feed from webcam 
cap = cv2.VideoCapture(0)
 
while True:
    #Reading each frame captured by the camera
    success, img = cap.read()
    #Resizing the image for fater processing 
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    #converting capture to RGB
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    

    #finding the locations of faces in the image 
    facesCurFrame = face_recognition.face_locations(imgS)
    #encoding the resize image face based on the face location data
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)


 #one by one it grabs a face location and the encoding from the encode face array 
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        #comparing the faces in the list of know faces and the with the encodeface from the webcam fame 
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        # finding the face distance, this will return a list of the distace of all your images you have stored, the lowest value will be the best match 
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        print(faceDis)
        #gives us the minimum value in our list, it will return the index i.e 0,1,2,3
        matchIndex = np.argmin(faceDis)


        #if there is a value in match index it will return true and the if statement will execute 
        if matches[matchIndex]:
            #changing the name to uppercase
            name = classNames[matchIndex].upper()
            #getting the location of the face 
            y1,x2,y2,x1 = faceLoc
            #scale our locations back up so we are able to have the rectage in the correct place 
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            #draw a rectagle on our original image 
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            #this will draw a filled rectage at the bottom of the image 
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            #this will put the name on the image where the filled rectager is located 
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
 
    cv2.imshow('F.R.A.T',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break