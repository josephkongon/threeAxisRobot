import math
from skimage.transform import (hough_line, hough_line_peaks)
import cv2
from object_detector import *
import numpy as np
from PIL import Image
from pyfirmata import Arduino, SERVO
from time import sleep
import threading

port = 'COM3'
pin10 = 10
pin9 = 9
board = Arduino(port)

board.digital[pin10].mode = SERVO
board.digital[pin9].mode = SERVO

motor1=0
motor2=0
# motor3=0

allmators= {(9,180),(10,180)}
reset ={9,10}

def rotateServer(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.015)


def getmotorAngle(pin):
    if (pin == 9):
        return motor1
    if (pin == 10):
        return motor2

def motorUp(pin, angle):
    global motor1
    global motor2
    before = getmotorAngle(pin)

    value=before - angle
    print(angle,before)
    if(angle>before):
        v= angle-before
        for i in range(before, angle,1):
            rotateServer(pin, i)
            if (pin == 9):
                motor1 = angle
            if (pin == 10):
                motor2 = angle


    if (angle<before):
        v =before - angle
        for i in range(before, angle, -1):
            rotateServer(pin, i)
            if (pin == 9):
                motor1 = angle
            if (pin == 10):
                motor2 = angle

for i in reset:
    rotateServer(i, 0)

for m in allmators:
    motorUp(m[0], 0)
    # motorUp(m[0],m[1])
    # motorUp(m[0], 20)
    # motorUp(m[0], 80)
    # motorUp(m[0], 0)
    # motorUp(m[0], 150)
    # motorUp(m[0], 0)
# load Aruco dectector

parameters = cv2.aruco.DetectorParameters_create()

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

cam = cv2.VideoCapture(1);



def gradient(pt1,pt2):
    try:
        return (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])
    except:
        return

def getangle(pointsList):
    a,b,c=pointsList[-3:]

    m1 = gradient(a,b)
    m2 = gradient(a,c )

    angle = math.atan((m2 - m1) / (1 + (m1 * m2)))
    angle = round(math.degrees(angle))
    if angle < 0:
        angle = 180 + angle
    print("angle",angle)

while True:

    _, img = cam.read();

    dimensions = img.shape

    # height, width, number of channels in image
    height, width, channels = img.shape

    ph=0.05 * height
    cw = math.floor(width / 2)
    ch = math.floor(height - ph)
    # print(cw,ch)

    cv2.drawMarker(img, (int(cw), int(ch)), (0, 0, 0), markerType=cv2.MARKER_SQUARE,
                   markerSize=40, thickness=2, line_type=cv2.LINE_8)

    # cv2.circle(img, ch, cw, (0, 0, 255), -1)

    # img= cv2.imread("phone_aruco_marker.jpg")

    # load object detectore

    detector = HomogeneousBgDetector()
    # get aruco marker
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters);

    if (corners):
        # drag pologone round the marker

        int_corners = np.int0(corners)
        cv2.polylines(img, int_corners, True, (0, 255, 0), 3)

        # aruco perimater

        aruco_peremeter = cv2.arcLength(corners[0], True)

        # pixel to cm ratio

        pixel_cm_ratio = aruco_peremeter / 20

        contours = detector.detect_objects(img)

        # Draw object boundries
        for cnt in contours:
            cv2.polylines((img), [cnt], True, (255, 0, 0), 2)

            # get rectangle
            # angle is very important
            rect = cv2.minAreaRect(cnt)

            (x, y), (w, h), angle = rect


            #print(x, y, w, h)
            # get the center point of each item
            cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)

            # get wight and height by applying the ration

            object_w = math.floor(w / pixel_cm_ratio)
            object_h = math.floor(h / pixel_cm_ratio)
            area = round(object_w * object_h)
            #print(area, "area")
            if(area<16 or area >26 ):
                print(area,  object_h,object_w)
                # here we get the correct recctangle of the object
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.polylines((img), [box], True, (255, 0, 0), 2)


                #create image
                image = np.zeros([height, width, 3],
                                 dtype=np.uint8)

                # setting RGB color values as 255,255,255
                image[:, :] = [0, 0, 0]

                # displaying the image

                cv2.line(image, (round(cw),round(ch)), (round(x),round(y)), (255, 255, 255), 2)
                cv2.line(image, (round(cw), round(ch)), ((0),(round(height-ph+5))), (255, 255, 255), 2)
                cv2.imshow("Line", image)



                image = np.mean(image, axis=2)

                # Perform Hough Transformation to detect lines
                hspace, angles, distances = hough_line(image)

                # Find angle
                angle = []
                for _, a, distances in zip(*hough_line_peaks(hspace, angles, distances)):
                    angle.append(a)

                # Obtain angle for each line
                angles = [a * 180 / np.pi for a in angle]

                # Compute difference between the two lines
                print(np.max(angles) , np.min(angles))
                angle_difference = np.max(angles) - np.min(angles)
                #print(180-angle_difference)
                angle =round(180-angle_difference)
                minangel=angle_difference

                dist = (math.sqrt((x - ch) ** 2 + (y - cw) ** 2)) / pixel_cm_ratio



                cv2.putText(img, "angle {} deg".format(round(angle, 1)), (int(x), int(y - 60)), cv2.FONT_HERSHEY_PLAIN, 1,
                            (100, 200, 0), 2)

                cv2.putText(img, "distance {} cm".format(round(dist, 1)), (int(x), int(y - 30)), cv2.FONT_HERSHEY_PLAIN, 1,
                            (100, 200, 0), 2)
                cv2.line(img, (int(x), int(y)), (int(cw), int(ch)), (0, 0, 0))
                cv2.putText(img, "width {} cm".format(round(object_w, 1)), (int(x), int(y - 15)), cv2.FONT_HERSHEY_PLAIN, 1,
                            (100, 200, 0), 2)
                cv2.putText(img, "height {} cm".format(round(object_h, 1)), (int(x), int(y + 20)), cv2.FONT_HERSHEY_PLAIN,
                            1, (100, 200, 0), 2)
                cv2.putText(img, "area {} cm**".format(round(area, 1)), (int(x), int(y + 60)), cv2.FONT_HERSHEY_PLAIN,1, (100, 200, 0), 2)
                # print(box)


                area = (w * h) / 100
                motorUp(pin9, angle)
                motorUp(pin10, angle)
                # print("angle ",angle, "with area of",area,"cm")

    cv2.imshow("contours", img)

    cv2.waitKey(1)
