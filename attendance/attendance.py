import cv2
import numpy as np
import face_recognition
import os
import time
from datetime import datetime

from PIL import ImageGrab

present_path=os.getcwd()
print(present_path)
path = os.path.join(present_path,'attendance','Training_images')
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []


    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def writeattendance(names):
    names=list(names)
    names.sort()
    textfile = open(os.path.join(present_path,'attendance','Attendance.txt'), "w")
    for element in names:
        textfile.write(element + "\n")
    textfile.close()

def captureScreen(bbox=(0,0,1920,1280)):
    capScr = np.array(ImageGrab.grab(bbox))
    capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
    return capScr

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

students=set()
start=time.time()
curr=time.time()
while True:
    curr=time.time()
    if curr>start+10:
        break
    # success, img = cap.read()
    img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
# print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()

            print(name)

            # y1, x2, y2, x1 = faceLoc
            # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            # cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            students.add(name)

    # cv2.imshow('Webcam', img)
    # cv2.waitKey(1)
# cap.release()
cv2.destroyAllWindows()
writeattendance(students)
print(list(students))