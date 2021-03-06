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

#cv2.imshow("blank",blank_image)    #show (d)Contours
#cv2.imshow("contour",contour_image)    #show (e)result
#cv2.imshow("contour_blur",contour_blur_image)    
#cv2.waitKey(0)

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


'''

indicate R0 R1 R2

'''

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

def least_squares_scaling_factors(k_vals):
    errs = []
    for i in xrange(len(lights)-1):
        for j in xrange(i+1, len(lights)):
            errs.append(
                k_vals[i]**2 * image_squared_distance[i] +\
                k_vals[j]**2 * image_squared_distance[j] -\
                2*k_vals[i]*k_vals[j] * pairwise_image_inner_products[i][j] -\
                transmitter_pair_squared_distance[i][j]
            )
        #errs = numpy.array(errs)
        #logger.debug('')
        #logger.debug('k_vals = {}'.format(k_vals))
        #logger.debug('errs = {}'.format(errs))
        #logger.debug('err2 = {}'.format(errs**2))
        #logger.debug('sum = {}'.format(sum(errs**2)))
        return errs

def scalar_scaling(k_vals):
        errs = numpy.array(least_squares_scaling_factors(k_vals))
        #print(numpy.sum(errs))
        return numpy.sum(errs)
    
def sol_guess_subset(index, var_cnt, sol_guess):
        sol_guess_sub = numpy.array([sol_guess[0,0]])
        for i in range(1,len(lights)):
            if sol_guess[i, 1] < 0:
                sol_guess_sub = numpy.append(sol_guess_sub, sol_guess[i, int((index%(2**var_cnt))/2**(var_cnt-1))])
                var_cnt -= 1
            else:
                sol_guess_sub = numpy.append(sol_guess_sub, sol_guess[i, 0])
        return sol_guess_sub
    
def brute_force_k():
        number_of_iteration = 500
        k0_vals = numpy.linspace(-0.1, -0.01, number_of_iteration)
        err_history = []
        idx_history = []
        k_vals = numpy.array([])
        for j in range(number_of_iteration+1):
            # Last iteration, Find minimum
            if (j==number_of_iteration):
                min_error_history_idx = err_history.index(min(err_history))
                min_idx = idx_history[min_error_history_idx]
                print("Using index ", min_idx, "for initial guess")
                k0_val = k0_vals[min_idx]
                #print(k0_val)
            else:
                k0_val = k0_vals[j]
            sol_guess = numpy.array([[k0_val, 0]])
            sol_found = 1
            multiple_sol = 0
            for i in range(1, len(lights)):
                sol = numpy.roots([image_squared_distance[i], -2*sol_guess[0,0]*pairwise_image_inner_products[0,i], (sol_guess[0,0]**2*image_squared_distance[0]-transmitter_pair_squared_distance[0, i])]);
                if numpy.isreal(sol)[0]:
                    if (sol[0] < 0) and (sol[1] < 0):
                        sol_guess = numpy.append(sol_guess, [sol], axis=0)
                        multiple_sol += 1
                    elif sol[0] < 0:
                        sol_guess = numpy.append(sol_guess, numpy.array([[sol[0], 0]]), axis=0)
                    elif sol[1] < 0:
                        sol_guess = numpy.append(sol_guess, numpy.array([[sol[1], 0]]), axis=0)
                    else:
                        sol_found = 0
                        break
                else:
                    sol_found = 0
                    break
            if sol_found:
                scaling_factors_error_combination = []
                #print ("index:", j)
                for m in range(1, 2**multiple_sol+1):
                    sol_guess_combination = sol_guess_subset(m, multiple_sol, sol_guess)
                    scaling_factors_error_arr = least_squares_scaling_factors(sol_guess_combination)
                    scaling_factors_error = 0
                    for n in scaling_factors_error_arr:
                        scaling_factors_error += n**2
                    scaling_factors_error_combination.append(scaling_factors_error)
                    #print("m: ", m, sol_guess_subset(m, multiple_sol, sol_guess), "error: ", scaling_factors_error)
                k_vals = sol_guess_subset(numpy.argmin(scaling_factors_error_combination)+1, multiple_sol, sol_guess)
                #print("mininum index", numpy.argmin(scaling_factors_error_combination), "K values: ", k_vals)
                if len(err_history)==0:
                    print ("First found index: ", j)
                err_history.append(min(scaling_factors_error_combination))
                idx_history.append(j)
        return k_vals
        # End of brute force method      

brute_force_k() 








