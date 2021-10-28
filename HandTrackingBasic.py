import cv2
import mediapipe as mp
import time
from HandTrackingModule import handDetector

cap = cv2.VideoCapture(0)

#setting up fps
preTime = 0
curTime = 0

#creating our class obj
detector = handDetector()

#need to do inorder to run webcam 
while True:
    success, img = cap.read()
    img = detector.findHands(img) #set draw to false if you dont want the dots and lines
    lmList = detector.findPosition(img, draw=False) #set draw to false if you dont want the dots and lines

    if len(lmList) != 0:
        #choose which land mark point you want printed
        print(lmList[4])

    #setting up fps
    curTime = time.time()
    fps = 1/(curTime - preTime)
    preTime = curTime

    #put fps on the img window 
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 225), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)