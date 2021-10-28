import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionConf=0.5, trackConf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConf = detectionConf
        self.trackConf = trackConf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils #draw on the hands

        self.tipIds = [4, 8, 12, 16]

    def findHands(self, img, draw=True):
        #convert to RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
        
        #If hand landmarks are detected then draw them on hand 
        if(self.results.multi_hand_landmarks):
            for handLms in self.results.multi_hand_landmarks:
                #if asked to draw by user then only draw
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNum=0, draw=True):
        #specific landmark list full of positions of all points on hand
        self.lmList = []
        
        #if landmarks detected then get those postions and add to list
        if self.results.multi_hand_landmarks:
            #only looking at hand provided by user 
            myHand = self.results.multi_hand_landmarks[handNum]
            #get all land marks for that hand 
            for id, lm in enumerate(myHand.landmark):
                    #getting pixle location values
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    #adds location and id point to list 
                    self.lmList.append([id, cx, cy])
                    #only draw if user wants to 
                    if draw: 
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return self.lmList

    def fingersUp(self):
        fingers = []

        #thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #other 4 fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] > self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, img, draw= True, r= 15, t= 3):
        #positions of two finger tips
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        #position of center of finger tips
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            #draw line
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            #draw circles on 2 finger tips
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            #draw center circle
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        #length of line between two finger tips
        length = math.hypot(x2, x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]




def main():
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

if __name__ == "__main__":
    main()