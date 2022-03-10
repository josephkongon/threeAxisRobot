import cv2
import numpy as np
import utilis

def nothing(X):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow('Tracking')
cv2.createTrackbar('LH','Tracking',0,255,nothing)
cv2.createTrackbar('LS','Tracking',0,255,nothing)
cv2.createTrackbar('LV','Tracking',0,255,nothing)
cv2.createTrackbar('UH','Tracking',255,255,nothing)
cv2.createTrackbar('US','Tracking',255,255,nothing)
cv2.createTrackbar('UV','Tracking',255,255,nothing)


while True:
    #for image input
    #normal = cv2.imread('balls.jpg')
    _,cam=cap.read()
    frame = cv2.resize(cam,(400,400))
    #convert to hvg image
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #getting the values from the tracbar
    lh = cv2.getTrackbarPos('LH','Tracking')
    ls = cv2.getTrackbarPos('LS', 'Tracking')
    lv = cv2.getTrackbarPos('LV', 'Tracking')

    uh = cv2.getTrackbarPos('UH', 'Tracking')
    us = cv2.getTrackbarPos('US', 'Tracking')
    uv = cv2.getTrackbarPos('UV', 'Tracking')
    #threshold the HSV image for arrage of BlueColor
    lowB = np.array([lh, ls,lv])
    upperB=np.array([uh,us,uv])
    #threshold the Hvg image to get only the blue color
    mask = cv2.inRange(hsv, lowB, upperB)

    res = cv2.bitwise_and(frame, frame,mask=mask)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()