import math

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# dpi for the saved figure: https://stackoverflow.com/a/34769840/3129414
dpi = 80

# Set red pixel value for RGB image
red = [1, 0, 0]
img = mpimg.imread('phone.jpg')
height, width, bands = img.shape

# Update red pixel value for RGBA image
if bands == 4:
    red = [1, 0, 0, 1]

w=math.floor(width/2)
h=math.floor(height/2)

# Update figure size based on image size
figsize = width / float(dpi), height / float(dpi)

# Create a figure of the right size with one axes that takes up the full figure
figure = plt.figure(figsize=figsize)
axes = figure.add_axes([0, 0, 1, 1])

# Hide spines, ticks, etc.
axes.axis('off')

# Draw a red dot at pixel (62,62) to (66, 66)
for i in range(w, h):
    for j in range(w, h):
        img[i][j] = red

# Draw the image
axes.imshow(img, interpolation='nearest')
cv2.imshow("contours", img)
#figure.savefig("test.png", dpi=dpi, transparent=True)
cv2.waitKey(0)