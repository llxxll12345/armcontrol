import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    #lower_blue = np.array([110,50,50])
    #upper_blue = np.array([130,255,255])

    lower_yellow = np.array([20, 50, 50])
    upper_yellow = np.array([30, 255, 255])

    # Threshold the HSV image to get only blue colors
    # mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask=mask)

    mask = cv2.resize(mask, (100, 100), interpolation=cv2.INTER_CUBIC)
    frame = cv2.resize(frame, (100, 100), interpolation=cv2.INTER_CUBIC)
    res = cv2.resize(res, (100, 100), interpolation=cv2.INTER_CUBIC)

    #concatenated = cv2.hconcat([frame, res])
    #cv2.imshow('con', concatenated)

    edge_filtered = cv2.Canny(res, 70, 100)
    #cv2.imshow('edge', edge_filtered)

    _, ctrs, hie = cv2.findContours(edge_filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for ctr in ctrs:
        area = cv2.contourArea(ctr)
        if area > 500:
            print(area)
            print("Found")


    #cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    #k = cv2.waitKey(5) & 0xFF
    #if k == 27:
    #    break

cv2.destroyAllWindows()