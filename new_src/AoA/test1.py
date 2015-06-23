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

#print freqs[0], freqs[1], freqs[2]

cv2.imshow("blank",blank_image)    #show (d)Contours
cv2.imshow("contour",contour_image)    #show (e)result
cv2.imshow("contour_blur",contour_blur_image)    
cv2.waitKey(0)

offset_z = 2.5 
Zf = 2  #light z coordinate is fixed by Zf

# add z coordinate to centers array 
centerlist0 = list(centers[0]) 
centerlist1 = list(centers[1]) 
centerlist2 = list(centers[2]) 

centerlist0.append(Zf)
centerlist1.append(Zf)
centerlist2.append(Zf)

centers[0] = tuple(centerlist0)
centers[1] = tuple(centerlist1)
centers[2] = tuple(centerlist2)

print "centers are :" , centers , "and radius are : " , radii 

# Compute squared distance from lens center to each projection
image_squared_distance = np.sum(np.square(centers), axis=1)
print "distance between lens_center to R0 R1 R2 are :" , image_squared_distance

# Compute pairwise constants (2*K_m*K_n term and abosulte square distances)
transmitters = [[2,5],[2.5,5.5],[3,5]]
transmitter_pair_squared_distance = [0,0,0]
pairwise_image_inner_products = [0,0,0]

transmitter_pair_squared_distance[0] = np.square(transmitters[0][0] - transmitters[1][0]) + np.square(transmitters[0][1] - transmitters[1][1])
transmitter_pair_squared_distance[1] = np.square(transmitters[1][0] - transmitters[2][0]) + np.square(transmitters[1][1] - transmitters[2][1])
transmitter_pair_squared_distance[2] = np.square(transmitters[2][0] - transmitters[0][0]) + np.square(transmitters[2][1] - transmitters[0][1])
print "squared distance (T0,T1) (T1,T2) (T2,T0) in real world :", transmitter_pair_squared_distance

pairwise_image_inner_products[0]= np.dot(centers[0], centers[1])
pairwise_image_inner_products[1]= np.dot(centers[1], centers[2])
pairwise_image_inner_products[2]= np.dot(centers[2], centers[0])
print  "inner products (R0.R1) (R1.R2) (R2.R0) :", pairwise_image_inner_products 

''' compute K0,K1,K2 '''




