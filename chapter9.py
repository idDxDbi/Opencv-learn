import cv2
import numpy as np
"""
人脸识别、追踪

FACE DETECTION
"""

faceCascade = cv2.CascadeClassifier("../Resources/haarcascade_frontalface_default.xml")
webcam = True
cap = cv2.VideoCapture(0)
cap.set(10,100)
cap.set(3,1920)
cap.set(4,1080)



path = "../Resources/lena.png"
while True:
    if webcam:
        success, img = cap.read()
    else:
        img = cv2.imread(path)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 进行面部级联


    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y),(x+w, y+h), (255,0,0), 2)
        cv2.putText(img, "boy", (x-10, y-10), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    0.75, (0, 255, 0), 2)



    cv2.imshow("Result", img)







    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

