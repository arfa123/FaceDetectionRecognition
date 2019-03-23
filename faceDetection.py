import cv2
import os
import sqlite3 as lite
from paths import getCurrentPath, getHaarcascadePath

def faceDetection(userName, userId, callBack):
    con = lite.connect('users.db')
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height
    face_detector = cv2.CascadeClassifier(getHaarcascadePath())
    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    os.mkdir(getCurrentPath()+"/dataset/"+userName+"."+str(userId))
    # Initialize individual sampling face count
    count = 0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/" + userName + "." + str(userId) + "/" + userName + "." + str(userId) + "." + str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 32:
            break
        elif count >= 30: # Take 30 face sample and stop video
            with con:
                cur = con.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS users(id INT, name TEXT)")
                cur.execute("INSERT INTO users VALUES(?, ?)", (userId, userName))
                con.commit()
            break
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    callBack()
    return userId+". "+userName