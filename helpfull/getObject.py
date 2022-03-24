import cv2
import numpy as np
from scipy.spatial import distance

sample_img = cv2.imread("square.jpg")

# convert to black and white color space
sample_img_grey = cv2.cvtColor(sample_img, cv2.COLOR_BGR2GRAY)
contours, hierarchy = cv2.findContours(sample_img_grey, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# find center of image and draw it (blue circle)
image_center = np.asarray(sample_img_grey.shape) / 2
image_center = tuple(image_center.astype('int32'))
cv2.circle(sample_img, image_center, 3, (255, 100, 0), 2)

buildings = []
for contour in contours:
    # find center of each contour
    M = cv2.moments(contour)
    center_X = int(M["m10"] / M["m00"])
    center_Y = int(M["m01"] / M["m00"])
    contour_center = (center_X, center_Y)

    # calculate distance to image_center
    distances_to_center = (distance.euclidean(image_center, contour_center))

    # save to a list of dictionaries
    buildings.append({'contour': contour, 'center': contour_center, 'distance_to_center': distances_to_center})

    # draw each contour (red)
    cv2.drawContours(sample_img, [contour], 0, (0, 50, 255), 2)
    M = cv2.moments(contour)

    # draw center of contour (green)
    cv2.circle(sample_img, contour_center, 3, (100, 255, 0), 2)

# sort the buildings
sorted_buildings = sorted(buildings, key=lambda i: i['distance_to_center'])

# find contour of closest building to center and draw it (blue)
center_building_contour = sorted_buildings[0]['contour']
cv2.drawContours(sample_img, [center_building_contour], 0, (255, 0, 0), 2)

cv2.imshow("Image", sample_img)
cv2.waitKey(0)