import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import skimage
from gaussian import GaussianImage, nms

def display_image(img):
    plt.imshow(img, cmap='gray')  
    plt.axis('off')      
    plt.show() 

# #Canny edge detector steps:
# Apply Gaussian filter to smooth the image in order to remove the noise
# Find the intensity gradients of the image
# Apply gradient magnitude thresholding or lower bound cut-off suppression to get rid of spurious response to edge detection
# Apply double threshold to determine potential edges
# Track edge by hysteresis: Finalize the detection of edges by suppressing all the other edges that are weak and not connected to strong edges.

#0) Import image and turn into greyscale:
img = cv.imread("test_images/woman_in_hallway.png", 0) #Read in file as greyscale img
# display_image(img)

#1) Apply gaussian filters to x and y

size = 3 
sigma = 2 #TODO: play around with these numbers to see what works best and not. 3,2 seem to be best

gaussian = GaussianImage(size, sigma, img)
# gaussian.show_filtered_images()
# display_image(gaussian.orientation)

#2) Find the intensity gradients of the image
magnitude = gaussian.magnitude
orientation = gaussian.orientation

#3) Non-maximum supression:
    #a Thin multi-pixel wide "ridges" to single pixel width
non_max_image = nms(orientation, magnitude)
display_image(non_max_image)

#4) Double thresholding




