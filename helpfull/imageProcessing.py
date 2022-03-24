
import numpy as np
import cv2

import utilis


webcam= False
path= 'image4.jpeg'
cap=cv2.VideoCapture(0)
cap.set(10,160)
cap.set(3,1920)
cap.set(4,1080)

scale =3;

wp=210*scale
hp=297*scale

scale =3;
while True:
    if webcam:succes,img=cap.read()
    else:img=cv2.imread(path)

    img, finalC= utilis.getContours(img,minArea=50000,filter=4)

    if len(finalC)!=0:
        biggest=finalC[0][2]
        #print(biggest)
        imgWarp=utilis.warp(img,biggest,wp,hp)
        #cv2.imshow('4A', imgWarp)

        imgC2, finalC2 = utilis.getContours(imgWarp, minArea=2000, filter=4,threatHold=[50,50],draw=False)

        if len(finalC) !=0:
            for obj in finalC2:
                cv2.polylines(imgC2,[obj[2]],True,(0,255,0),2)
                nPonts=utilis.reorder(obj[2])
                newW=round(utilis.findDis(nPonts[0][0]//scale,nPonts[1][0]//scale)/10)
                newH=round(utilis.findDis(nPonts[0][0]//scale,nPonts[2][0]//scale)/10)

                cv2.arrowedLine(imgC2,(nPonts[0][0][0], nPonts[0][0][1]),(nPonts[1][0][0],nPonts[1][0][1]),
                                (255,0,255),3,8,0,0.05)
                cv2.arrowedLine(imgC2, (nPonts[0][0][0], nPonts[0][0][1]), (nPonts[2][0][0], nPonts[2][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                x,y,w,h=obj[3]


                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 0.9
                fontColor = (255, 0, 255)
                org = (x+30,y-10)
                text = "{}cm".format(newW)

                cv2.putText(imgC2, text, org, font, fontScale, fontColor)
                #cv2.putText(imgC2,"{}cm".format(newW), (x+30,y-10),cv2.FONT_HERSHEY_COMPLEX,(255,0,255),3)
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 0.9
                fontColor = (255, 0, 255)
                org = (x - 70, y + h//2)
                text = "{}cm".format(newH)

                cv2.putText(imgC2, text, org, font, fontScale, fontColor)
               # cv2.putText(imgC2, '{}cm'.format(newH), (x + 70, y - h//2), cv2.FONT_HERSHEY_COMPLEX, (255, 0, 255), 3)

        cv2.imshow('inner', imgC2)

    img= cv2.resize(img,(0,0),None,0.5,0.5)
    cv2.imshow('Original',img)
    cv2.waitKey(1)




