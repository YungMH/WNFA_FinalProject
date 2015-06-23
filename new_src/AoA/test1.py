import math 
import numpy as np
import cv2


# Load an color image in grayscale
img = cv2.imread('001.png',0)
gray_image = cv2.imread('001.png', cv2.IMREAD_GRAYSCALE)

m2 = cv2.blur(img, (50,50)) # faster and good enough
threshold, thresholded_img = cv2.threshold(m2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
contours, heirarchy = cv2.findContours(thresholded_img, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#contours, heirarchy = cv2.findContours(thresholded_img, 1,2)

#draw contours 
contour_image = gray_image.copy()
cv2.drawContours(contour_image, contours, -1, 255, 3)
contour_blur_image = m2.copy()
cv2.drawContours(contour_blur_image, contours, -1, 255, 3)
dim = (gray_image.shape[0], gray_image.shape[1], 3)
blank_image = np.zeros(dim, np.uint8)
cv2.drawContours(blank_image, contours, -1, (255,255,255), 3)

#start get center and radius
centers = []
radii = []
freqs = []
cnt = 0

for contour in contours:
    center, radius = cv2.minEnclosingCircle(contour)
    center = map(int, center)
    radius = int(radius)
    
    center = (center[0] , center[1])
    contour_area = cv2.contourArea(contour)
    circle_area = math.pi * radius**2

    centers.append(center)
    radii.append(radius)

print centers
print radii

cv2.imshow("blank",blank_image)    #show (d)Contours
cv2.imshow("contour",contour_image)    #show (e)result
cv2.imshow("contour_blur",contour_blur_image)    


cv2.waitKey(0)

