import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

#creating width and height parameters
wCam, hCam = 640, 480

cTime = 0
pTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionConf=0.7)


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    
    #list of all the postions of the points on the hand
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8]) #points for tip of the thumb and fist finger 

        thumb_x, thumb_y = lmList[4][1], lmList[4][2]
        firstFinger_x, firstFinger_y = lmList[8][1], lmList[8][2]
        #center position of line
        cx, cy = (thumb_x + firstFinger_x) // 2, (thumb_y + firstFinger_y) // 2

        #creating circles around thumb and first finger points and center of line
        cv2.circle(img, (thumb_x, thumb_y), 12, (225, 0, 225), cv2.FILLED)
        cv2.circle(img, (firstFinger_x, firstFinger_y), 12, (225, 0, 225), cv2.FILLED)
        cv2.circle(img, (cx, cy), 12, (225, 0, 225), cv2.FILLED)

        #create line between them
        cv2.line(img, (thumb_x, thumb_y), (firstFinger_x, firstFinger_y), (225, 0 ,0), 3)

        length = math.hypot(thumb_x - firstFinger_x, thumb_y - firstFinger_y)
        print(length)

        if length < 20:
            cv2.circle(img, (cx, cy), 12, (0, 0, 0), cv2.FILLED)

        

    #setting up fps
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    #put fps on the img window 
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

    cv2.imshow("Img", img)
    cv2.waitKey(1)

