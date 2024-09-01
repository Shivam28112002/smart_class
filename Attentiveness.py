# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import playsound
import argparse
import imutils
import time
import dlib
import cv2 as cv
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import time
import json

ctime=0
ptime=0

idList = [22,23,24,26,110,157,158,159,160,161,130,243]
ratioList = []
blinkCounter = 0
counter = 0
attentionCounter = 0
countatt = 0
x=0

cap=cv.VideoCapture(0) # Screencapture
detector = FaceMeshDetector(maxFaces=1) #maxFaces= n_maxFaces
plotY = LivePlot(640,480,[20,50],invert=True)

while True:
    if x==0:
        ptime=time.time()
    x=1
    # if cap.get(cv.CAP_PROP_PROS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT) :
    #     cap.set(cv.CAP_PROP_PROS_FRAMES,0)
    
    success, img=cap.read()
    img,faces = detector.findFaceMesh(img,draw=False)

    if faces:
        face  = faces[0]
        for id in idList:
            cv.circle(img,face[id],2,(255,0,255),cv.FILLED)
        leftUp= face[159]
        leftDown= face[23]
        leftLeft  =  face[130]
        leftRight= face[243]
        lenghtVer,_ = detector.findDistance(leftUp,leftDown)
        lenghtHor,_ = detector.findDistance(leftLeft,leftRight)
        ratio= int((lenghtVer/lenghtHor)*100)
        ratioList.append(ratio)
        if(len(ratioList)>10): 
            ratioList.pop(0)
        ratioAvg = sum(ratioList)/len(ratioList)

        if ratioAvg<=35 and counter == 0:
            blinkCounter+=1
            counter=1
        if counter!=0:
            counter+=1
            if counter>10:
                counter=0

        cvzone.putTextRect(img,f'Blink Count: {blinkCounter}',(0,100))

        if ratioAvg>50 or ratioAvg<25:
            if countatt==0:
                attentionCounter+=1
                countatt=1
            cvzone.putTextRect(img,f'Attention Lost ! : {attentionCounter}',(0,100))
        else:
            countatt= 0


        imPlot = plotY.update(ratioAvg)
        cv.imshow("image plot",imPlot)
        # print(ratio)
        cv.resize(img,(640,360))
        imgstack= cvzone.stackImages([img,imPlot],2,1)
    else:
        cv.resize(img,(640,360))
        imgstack = cvzone.stackImages([img,img],2,1)
        if countatt==0:
            attentionCounter+=1
            countatt=1
        cvzone.putTextRect(img,f'Attention Lost ! : {attentionCounter}',(0,100))

    cv.imshow("Uniillusionque Brains",img)
    cv.waitKey(1)
    if cv.waitKey(1) & 0xFF == 27:
        break

ctime = time.time()
avgattention = attentionCounter/(ctime-ptime)
avgblink = blinkCounter/(ctime-ptime)
print(ctime-ptime)

if avgattention <= 0.167:
    s = "Has good posture"
elif avgattention<=0.34 and avgattention>0.167:
    s= "Avarage body movement"
else:
    s="Poor focus high body movement"

if avgblink >=0.167 and avgblink<=0.47:
    t = "Don't feel drowsy during class"
else:
    t="Feels drowsy during class"

if avgblink*avgattention <= 0.212:
    u="Attentive"
else:
    u="Not Attentive"

mydict = {"Posture" : s, "Blinking":t,"Attentiveness": u}
with open('convert.txt', 'w') as convert_file:
     convert_file.write(json.dumps(mydict))
cap.release()
