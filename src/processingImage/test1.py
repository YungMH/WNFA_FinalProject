import math 
import numpy as np
import cv2


# Load an color image in grayscale
img = cv2.imread('001.png',0)
m2 = cv2.blur(img, (50,50)) # faster and good enough
threshold, thresholded_img = cv2.threshold(m2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
contours, heirarchy = cv2.findContours(thresholded_img, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow("img",thresholded_img)
cv2.waitKey(0)