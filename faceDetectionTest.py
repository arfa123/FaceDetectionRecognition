import numpy as np
import cv2
from paths import getHaarcascadePath

def testCamera(callBack, userName, userId, callBack2):
    print("testing Caemras")
    faceCascade = cv2.CascadeClassifier(getHaarcascadePath())
    cap = cv2.VideoCapture(0)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    font = cv2.FONT_HERSHEY_SIMPLEX
    k = 255
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,     
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20)
        )
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            cv2.putText(img, "Press Enter to Continue & q to Quit", (x+5,y-5), font, 1, (255,255,255), 1)
        cv2.imshow('video',img)
        k = cv2.waitKey(30) & 0xff
        if k == 13 or k == 113: #q=113
            break
    cap.release()
    cv2.destroyAllWindows()
    if k == 13: # press 'Enter' to quit
        val = callBack(userName, userId, callBack2)
        return val