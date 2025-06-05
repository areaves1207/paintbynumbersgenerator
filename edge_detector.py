import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import skimage
from gaussian import GaussianImage, nms
from threshing import thresh
from hysteresis import hysteresis

def display_image(img, title="figure"):
    plt.title(title)
    plt.imshow(img, cmap='gray')  
    plt.axis('off')      
    plt.show() 

# # #Canny edge detector steps:
# # Apply Gaussian filter to smooth the image in order to remove the noise
# # Find the intensity gradients of the image
# # Apply gradient magnitude thresholding or lower bound cut-off suppression to get rid of spurious response to edge detection
# # Apply double threshold to determine potential edges
# # Track edge by hysteresis: Finalize the detection of edges by suppressing all the other edges that are weak and not connected to strong edges.
# # def detect_edges(image_name=""):
# #0) Import image and turn into greyscale:
# img = cv.imread("test_images/1920x1080.jpg", 0) #Read in file as greyscale img
# # display_image(img)

# #1) Apply gaussian filters to x and y
# size = 25
# sigma = 5 #TODO: play around with these numbers to see what works best and not. 5,2 seems to be best

# gaussian = GaussianImage(size, sigma, img)
# # gaussian.show_filtered_images()
# # display_image(gaussian.orientation)

# #2) Find the intensity gradients of the image
# magnitude = gaussian.magnitude
# orientation = gaussian.orientation

# #3) Non-maximum supression:
#     #a Thin multi-pixel wide "ridges" to single pixel width
# non_max_image = nms(orientation, magnitude)
# # display_image(non_max_image)

# #4) Double thresholding
# thresh, strong_edges, weak_edges = thresh(non_max_image, 50, 150) #TODO: has 2 optional params, low and high. Play around with these

# #Hysteresis; follow edges to connect strong to weak edges
# hyst = hysteresis(strong_edges, weak_edges)

# #Connect patches
# # final = cv.morphologyEx(hyst, cv.MORPH_GRADIENT, np.ones((3, 3), np.uint8))


# #DISPLAY STEPS
# # display_image(strong_edges,  "Strong edges")
# # display_image(weak_edges, "Weak edges")
# # display_image(thresh, "Threshing")
# display_image(hyst, "Hystersis Completed")
# # xdisplay_image(final, "Connected Patches")

