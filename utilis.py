
import cv2
import numpy as np

def getContours(img,threatHold=[100,100],show=False, minArea=1000,filter=0,draw=False):
    imgGray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny =cv2.Canny(imgBlur,threatHold[0],threatHold[1])
    kernel=np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=3)
    imgThre=cv2.erode(imgDial,kernel,iterations=2)
    if show:cv2.imshow("Canny",imgThre)

    contoures, hiearchy = cv2.findContours(imgThre,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    finalCountours=[]
    for i in contoures:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i,True)
            approx= cv2.approxPolyDP(i,0.02*peri,True)
            bbox=cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalCountours.append((len(approx),area,approx,bbox,i))
            else:
                finalCountours.append((len(approx), area, approx, bbox, i))

    finalCountours =sorted(finalCountours,key = lambda x:x[1],reverse=True)

    if draw:
        for con in finalCountours:
            cv2.drawContours(img,con[4],-1,(0,0,255),3)
    #cv2.imshow('inner', img)
    return img, finalCountours

def reorder(points):
    #print(points.shape)
    newP=np.zeros_like(points)
    points=points.reshape((4,2))
    add=points.sum(1)
    newP[0]=points[np.argmin(add)]
    newP[3] = points[np.argmax(add)]
    diff= np.diff(points,axis=1)
    newP[1]=points[np.argmin(diff)]
    newP[2] = points[np.argmax(diff)]
    return newP

def warp(img,poins,w,h, pad=20):
    #print(poins)
    #print(reorder(poins))
    poins=reorder(poins)
    pts1=np.float32(poins)
    pts2=np.float32([[0,0],[w,0],[0,h],[w,h]])
    matrix=cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp=cv2.warpPerspective(img,matrix,(w,h))
    imgWarp = imgWarp[pad:imgWarp.shape[0]-pad,pad:imgWarp.shape[1]-pad]
    return imgWarp


def findDis(pt1,pt2):
    return ((pt2[0]-pt1[0])**2+(pt2[1]-pt1[1])**2)**0.5

