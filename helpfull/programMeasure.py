import math
from skimage.transform import (hough_line, hough_line_peaks)
import cv2
from object_detector import *
import numpy as np
from PIL import Image

# load Aruco dectector

parameters = cv2.aruco.DetectorParameters_create()

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

cam = cv2.VideoCapture(1);


def edge_detection(img, blur_ksize=5, threshold1=70, threshold2=200):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gaussian = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    img_canny = cv2.Canny(img_gaussian, threshold1, threshold2)

    return img_canny

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

            object_w = w / pixel_cm_ratio
            object_h = h / pixel_cm_ratio
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
            cv2.line(image, (round(cw), round(ch)), ((0),(round(height))), (255, 255, 255), 2)
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
            angle_difference = np.max(angles) - np.min(angles)
            #print(180-angle_difference)


            dist = (math.sqrt((x - ch) ** 2 + (y - cw) ** 2)) / pixel_cm_ratio

            print(dist)



            #print(round(dist))

            # cv2.putText(img, "angle {} deg".format(round(ang, 1)), (int(x), int(y - 40)), cv2.FONT_HERSHEY_PLAIN, 1,
            #             (100, 200, 0), 2)

            cv2.putText(img, "distance {} cm".format(round(dist, 1)), (int(x), int(y - 35)), cv2.FONT_HERSHEY_PLAIN, 1,
                        (100, 200, 0), 2)
            cv2.line(img, (int(x), int(y)), (int(cw), int(ch)), (0, 0, 0))
            cv2.putText(img, "width {} cm".format(round(object_w, 1)), (int(x), int(y - 15)), cv2.FONT_HERSHEY_PLAIN, 1,
                        (100, 200, 0), 2)
            cv2.putText(img, "height {} cm".format(round(object_h, 1)), (int(x), int(y + 20)), cv2.FONT_HERSHEY_PLAIN,
                        1, (100, 200, 0), 2)
            # cv2.putText(img, "angle {} deg".format(round(angle, 1)), (int(x), int(y + 30)), cv2.FONT_HERSHEY_PLAIN,1, (100, 200, 0), 2)
            # print(box)

            area = (w * h) / 100
            # print("angle ",angle, "with area of",area,"cm")

    cv2.imshow("contours", img)

    cv2.waitKey(1)
