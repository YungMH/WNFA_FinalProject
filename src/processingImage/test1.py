import math 
import numpy as np
import cv2


# Load an color image in grayscale
img = cv2.imread('001.png',0)
m2 = cv2.blur(img, (50,50)) # faster and good enough
threshold, thresholded_img = cv2.threshold(m2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
contours, heirarchy = cv2.findContours(thresholded_img, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#contours, heirarchy = cv2.findContours(thresholded_img, 1,2)

#print contours 

centers = []
radii = []
freqs = []
cnt = 0

for contour in contours:
    center, radius = cv2.minEnclosingCircle(contour)
    center = map(int, center)
    radius = int(radius)
    
center = (center[1], center[0])
contour_area = cv2.contourArea(contour)
circle_area = math.pi * radius**2

centers.append(center)
radii.append(radius)

print centers


cv2.imshow("img",thresholded_img)
cv2.waitKey(0)

