import numpy as np
from scipy.spatial import distance as dist
import cv2
from imutils import contours
from imutils import perspective
import imutils
def show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def midpoint(ptA,ptB):
    return ((ptA[0] + ptB[0]) * 0.5 , (ptA[1] + ptB[1]) * 0.5)
img = cv2.imread('redBlack.png')
width = 25
img = imutils.resize(img,height = 500)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray,(5,5),0)
edged = cv2.Canny(gray,70,200)
edged = cv2.dilate(edged,None,iterations = 1)
edged = cv2.erode(edged,None,iterations = 1)
cnts,_ = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
(cnts,_) = contours.sort_contours(cnts)

pixelPerMetricX = 0
pixelPerMetricY = 0
order = 1
for c in cnts:
    if cv2.contourArea(c) < 100:
        continue
    orig = img.copy()
    box = cv2.minAreaRect(c)
    box = cv2.boxPoints(box)
    box = box.astype('int')
    box = perspective.order_points(box)
    cv2.drawContours(orig,[box.astype(int)],0,(0,255,0),2)
    print(box)

    for x,y in box:
        cv2.circle(orig,(int(x),int(y)),5,(0,0,255),3)
        (tl,tr,br,bl) = box
        (tltrX,tltrY) = midpoint(tl,tr)
        (tlblX,tlblY) = midpoint(tl,bl)
        (blbrX,blbrY) = midpoint(bl,br)
        (trbrX,trbrY) = midpoint(tr,br)
        cv2.circle(orig,(int(tltrX),int(tltrY)),5,(183,197,57),-1)
        cv2.circle(orig,(int(tlblX),int(tlblY)),5,(183,197,57),-1)
        cv2.circle(orig,(int(blbrX),int(blbrY)),5,(183,197,57),-1)
        cv2.circle(orig,(int(trbrX),int(trbrY)),5,(183,197,57),-1)
        cv2.line(orig,(int(tltrX),int(tltrY)),(int(blbrX),int(blbrY)),(255,0,0),2)
        cv2.line(orig,(int(tlblX),int(tlblY)),(int(trbrX),int(trbrY)),(255,0,0),2)

        # The longitudinal
        dA = dist.euclidean((tltrX,tltrY),(blbrX,blbrY))
        # The transverse
        dB = dist.euclidean((tlblX,tlblY),(trbrX,trbrY))

        if pixelPerMetricX == 0 or pixelPerMetricY == 0:
            pixelPerMetricX = dB / width
            pixelPerMetricY = dA / width
            dimA = dA / pixelPerMetricY
            dimB = dB / pixelPerMetricX
            print(dimB,dimB)
            cv2.putText(orig,"{:.1f}mm".format(dimB),(int(tltrX)-10,int(tltrY)),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
            cv2.putText(orig,"{:.1f}mm".format(dimA),(int(trbrX)-10,int(trbrY)),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
            cv2.imwrite('{}.jpg'.format(order),orig)
            cv2.imshow("Image", orig)
           # order += 1
            cv2.waitKey(0)