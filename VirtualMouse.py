import cv2
import numpy as np
import HandTrackingModule as htm
import time
import mouse
import pyautogui as pag 

# 6:36

wCam, hCam = 640, 480 #creating width and height parameters
frameR = 150 #frame reduction
smoothening = 5 #smoothen value

wScr, hScr = pag.size() #screen size

cTime = 0 #curent time
pTime = 0 #previous time
plocX, plocY = 0, 0 #current x location 
clocX, clocY = 0, 0 #current y location

cap = cv2.VideoCapture(0) #your laptop camera 
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionConf=0.7)


while True:
    success, img = cap.read()
    #img = cv2.flip(img, 1)
    img = detector.findHands(img)
    
    #list of all the postions of the points on the hand
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        fingersList = detector.fingersUp()
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
       

        

        #frame reduction 
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        if(fingersList == [0, 1, 0, 0, 0]):
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            
            #converting coordinates 
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            #smoothened values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            #move the mouse
            mouse.move(wScr - clocX, clocY, absolute=True, duration=0) 
            plocX, plocY = clocX, clocY  

        if(fingersList == [0, 1, 1, 0, 0]):
            distance = detector.findDistance(8, 12, img)
            length = distance[0]

            #draw center circle  and make it red
            cv2.circle(img, (distance[2][4], distance[2][5]), 5, (0, 0, 255), cv2.FILLED)
            if(length < 15):
                mouse.click(button='left')
                #draw circle black if "clicked"
                cv2.circle(img, (distance[2][4], distance[2][5]), 5, (0, 0, 0), cv2.FILLED)
                print("Right click!")

        if(fingersList == [0, 0, 0, 0, 1]):
            pag.scroll(100)
            print("Scroll up!")
        if(fingersList == [1, 0, 0, 0, 0]):
            pag.scroll(-100)
            print("Scroll down!")

        #print(fingersList)


        

    #setting up fps
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    #put fps on the img window 
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

    cv2.imshow("Img", img)
    cv2.waitKey(1)

