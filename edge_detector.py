import cv2 as cv

# #Canny edge detector steps:
# Apply Gaussian filter to smooth the image in order to remove the noise
# Find the intensity gradients of the image
# Apply gradient magnitude thresholding or lower bound cut-off suppression to get rid of spurious response to edge detection
# Apply double threshold to determine potential edges
# Track edge by hysteresis: Finalize the detection of edges by suppressing all the other edges that are weak and not connected to strong edges.

#0) Import image and turn into greyscale:
img = cv.imread("test_images/woman_in_hallway.png", 0) #Read in file as greyscale img

cv.imshow('Grayscale Image', img)
cv.waitKey(0)
cv.destroyAllWindows()

#1) Apply gaussian filters to x and y