import cv2
import numpy as np
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import utilis

class Processes:




    scale = 3;
    def nothing(X):
        pass
    def back(*args):
        pass

    def getDistance(res):
        def midpoint(ptA, ptB):
            return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

        # construct the argument parse and parse the arguments
        ap = argparse.ArgumentParser()
        # ap.add_argument("-i", "./", required=True,
        #                 help="path to the input image")
        # ap.add_argument("-w", "2", type=float, required=True,
        #                 help="width of the left-most object in the image (in inches)")
        args = vars(ap.parse_args())

        # load the image, convert it to grayscale, and blur it slightly
        image = res
        cv2.imshow("", image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        cv2.imshow("", gray)

        # perform edge detection, then perform a dilation + erosion to
        # close gaps in between object edges
        edged = cv2.Canny(gray, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

        # find contours in the edge map
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # sort the contours from left-to-right and, then initialize the
        # distance colors and reference object
        (cnts, _) = contours.sort_contours(cnts)
        colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255), (255, 255, 0),
                  (255, 0, 255))
        refObj = None

        # loop over the contours individually
        for c in cnts:
            # if the contour is not sufficiently large, ignore it
            if cv2.contourArea(c) < 100:
                continue

            # compute the rotated bounding box of the contour
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")

            # order the points in the contour such that they appear
            # in top-left, top-right, bottom-right, and bottom-left
            # order, then draw the outline of the rotated bounding
            # box
            box = perspective.order_points(box)

            # compute the center of the bounding box
            cX = np.average(box[:, 0])
            cY = np.average(box[:, 1])

            # if this is the first contour we are examining (i.e.,
            # the left-most contour), we presume this is the
            # reference object
            if refObj is None:
                # unpack the ordered bounding box, then compute the
                # midpoint between the top-left and top-right points,
                # followed by the midpoint between the top-right and
                # bottom-right
                (tl, tr, br, bl) = box
                (tlblX, tlblY) = midpoint(tl, bl)
                (trbrX, trbrY) = midpoint(tr, br)

                # compute the Euclidean distance between the midpoints,
                # then construct the reference object
                D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                refObj = (box, (cX, cY), D / 2.5)
                continue

            # draw the contours on the image
            orig = image.copy()
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
            cv2.drawContours(orig, [refObj[0].astype("int")], -1, (0, 255, 0), 2)

            # stack the reference coordinates and the object coordinates
            # to include the object center
            refCoords = np.vstack([refObj[0], refObj[1]])
            objCoords = np.vstack([box, (cX, cY)])

            # loop over the original points
            for ((xA, yA), (xB, yB), color) in zip(refCoords, objCoords, colors):
                # draw circles corresponding to the current points and
                # connect them with a line
                cv2.circle(orig, (int(xA), int(yA)), 5, color, -1)
                cv2.circle(orig, (int(xB), int(yB)), 5, color, -1)
                cv2.line(orig, (int(xA), int(yA)), (int(xB), int(yB)),
                         color, 2)
                # compute the Euclidean distance between the coordinates,
                # and then convert the distance in pixels to distance in
                # units
                D = dist.euclidean((xA, yA), (xB, yB)) / refObj[2]
                (mX, mY) = midpoint((xA, yA), (xB, yB))
                cv2.putText(orig, "{:.1f}in".format(D), (int(mX), int(mY - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

                # show the output image
                cv2.imshow("Image", orig)
                #cv2.waitKey(0)

    def getArea(res):
        scale = 3;

        wp = 210 * scale
        hp = 297 * scale
        img, finalC = utilis.getContours(res, minArea=20000, filter=4)
        print(finalC)
        if len(finalC) != 0:
            biggest = finalC[0][2]
            # print(biggest)
            imgWarp = utilis.warp(img, biggest, wp, hp)
            # cv2.imshow('4A', imgWarp)

            imgC2, finalC2 = utilis.getContours(imgWarp, minArea=2000, filter=4, threatHold=[50, 50], draw=False)
            print(finalC2)
            if len(finalC) != 0:
                print("heererer")
                for obj in finalC2:
                    cv2.polylines(imgC2, [obj[2]], True, (0, 255, 0), 2)
                    nPonts = utilis.reorder(obj[2])
                    newW = round(utilis.findDis(nPonts[0][0] // scale, nPonts[1][0] // scale) / 10)
                    newH = round(utilis.findDis(nPonts[0][0] // scale, nPonts[2][0] // scale) / 10)

                    cv2.arrowedLine(imgC2, (nPonts[0][0][0], nPonts[0][0][1]), (nPonts[1][0][0], nPonts[1][0][1]),
                                    (255, 0, 255), 3, 8, 0, 0.05)
                    cv2.arrowedLine(imgC2, (nPonts[0][0][0], nPonts[0][0][1]), (nPonts[2][0][0], nPonts[2][0][1]),
                                    (255, 0, 255), 3, 8, 0, 0.05)
                    x, y, w, h = obj[3]

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 0.9
                    fontColor = (255, 0, 255)
                    org = (x + 30, y - 10)
                    text = "{}cm".format(newW)

                    cv2.putText(imgC2, text, org, font, fontScale, fontColor)
                    # cv2.putText(imgC2,"{}cm".format(newW), (x+30,y-10),cv2.FONT_HERSHEY_COMPLEX,(255,0,255),3)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 0.9
                    fontColor = (255, 0, 255)
                    org = (x - 70, y + h // 2)
                    text = "{}cm".format(newH)

                    cv2.putText(imgC2, text, org, font, fontScale, fontColor)
                # cv2.putText(imgC2, '{}cm'.format(newH), (x + 70, y - h//2), cv2.FONT_HERSHEY_COMPLEX, (255, 0, 255), 3)

            cv2.imshow('inner', imgC2)

        img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
        cv2.imshow('Original', img)
        cv2.waitKey(1)

    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Tracking',cv2.WINDOW_NORMAL)
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

        #cv2.imshow('frame', frame)
        #cv2.imshow('mask', mask)
        cv2.imshow('res', res)
        key = cv2.waitKey(1)

        #cv2.imshow('res', res)


        ret, frame = cap.read()

        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray)

        getArea(res)
        getDistance(res)



        if key == 27:
            break


    cap.release()
    cv2.destroyAllWindows()