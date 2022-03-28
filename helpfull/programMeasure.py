import cv2
from object_detector import *
import numpy as np



#load Aruco dectector

parameters = cv2.aruco.DetectorParameters_create()

aruco_dict=cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)


img= cv2.imread("phone_aruco_marker.jpg")

#load object detectore

detector= HomogeneousBgDetector()
#get aruco marker
corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img,aruco_dict,parameters=parameters);

if(corners):
    #drag pologone round the marker
    int_corners= np.int0(corners)
    cv2.polylines(img,int_corners,True, (0,255,0),3)

    #aruco perimater

    aruco_peremeter=cv2.arcLength(corners[0],True)

    #pixel to cm ratio

    pixel_cm_ratio= aruco_peremeter / 20




    contours = detector.detect_objects(img)

    #Draw object boundries
    for cnt in contours:

        cv2.polylines((img),[cnt],True,(255,0,0),2)

        #get rectangle
        #angle is very important
        rect=cv2.minAreaRect(cnt)
        (x,y),(w,h),angle=rect

        #get the center point of each item
        cv2.circle(img,(int(x),int(y)),5,(0,0,255),-1)

        #get wight and height by applying the ration

        object_w=w/pixel_cm_ratio
        object_h=h/pixel_cm_ratio
        #here we get the correct recctangle of the object
        box=cv2.boxPoints(rect)
        box=np.int0(box)
        cv2.polylines((img), [box], True, (255, 0, 0), 2)

        cv2.putText(img, "width {} cm".format(round(object_w,1)),(int(x),int(y-15)),cv2.FONT_HERSHEY_PLAIN,1,(100,200,0),2)
        cv2.putText(img, "height {} cm".format(round(object_h, 1)), (int(x), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
        print(box)


        area=(w*h)/100
        print("angle ",angle, "with area of",area,"cm")




    cv2.imshow("contours",img)

    cv2.waitKey(0)