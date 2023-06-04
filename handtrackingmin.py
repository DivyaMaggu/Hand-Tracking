"""
Mediapipe- is a framework designed by google, here we're working with hand tracking model which uses two modules 
at backend i.e. Palm detection and hand landmarks. Palm detection - works on a complete image & it basically 
provides a cropped image of the hand and from there the hand landmarks module finds 21 different landmarks on 
this cropped image of the hand.
"""
import cv2
import mediapipe as mp
import time     

cam = cv2.VideoCapture(0)    
mpHands = mp.solutions.hands
hands = mpHands.Hands()                         # creates object for mpHands to detect the hands.
mpDraw = mp.solutions.drawing_utils

pTime = 0                                            # used to record the time when we processed last frame
cTime = 0                                            # used to record the time at which we processed current frame


while (cam.isOpened()):
    success, img = cam.read()
    if success==True:                            # storing frames in img variable
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)       # converting bgr img to rgb as hand detection recognize rgb img
        results = hands.process(img_RGB)
    else:
        break

    if results.multi_hand_landmarks:                        # if hands detected in results true
        for handLms in results.multi_hand_landmarks:        # for loop is to iterate over if more than 1 hand is there
            
            """
            Try to find some information within these captured hands - landmarks and id 
            Landmarks will give us the x and y coordinates.
            Ids of the landmarks, already they are listed in correct order, we've to check the index number only."""
            
            for id , lm in enumerate(handLms.landmark):
                # print(id , lm)
                h, w, c = img.shape                        # getting the height width and channel of image
                cx, cy = int(lm.x*w), int(lm.y*h)          # location of landmarks in pixel values
                print(id, cx, cy)

                if id == 4:
                    cv2.circle(img, (cx,cy), 5, (255,0,255), cv2.FILLED)           
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)       # It'll draw hand connections on hand
            
    # Calculating frame per second of webcam-
    cTime = time.time()              # time when we finish processing for this frame
    fps = 1/(cTime-pTime)
    pTime = cTime

    # Displaying fps on screen-
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)
    
    
    cv2.imshow("Hand Tracking",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):    # press 'Q' if you want to exit
        break
 

cam.release()                       # When everything done, release the capture
cv2.destroyAllWindows()             # Destroy the all windows now