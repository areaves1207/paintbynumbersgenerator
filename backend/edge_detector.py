import matplotlib.pyplot as plt
import numpy as np
from gaussian import GaussianImage, nms, hysteresis, thresh

# # #Canny edge detector steps:
# # Apply Gaussian filter to smooth the image in order to remove the noise
# # Find the intensity gradients of the image
# # Apply gradient magnitude thresholding or lower bound cut-off suppression to get rid of spurious response to edge detection
# # Apply double threshold to determine potential edges
# # Track edge by hysteresis: Finalize the detection of edges by suppressing all the other edges that are weak and not connected to strong edges.
def detect_edges_canny(img):
    #1) Apply gaussian filters to x and y
    size = 25
    sigma = 1.4

    gaussian = GaussianImage(size, sigma, img)
    # gaussian.show_filtered_images()
    # display_image(gaussian.orientation)

    #2) Find the intensity gradients of the image
    magnitude = gaussian.magnitude
    orientation = gaussian.orientation

    #3) Non-maximum supression:
        #a Thin multi-pixel wide "ridges" to single pixel width
    non_max_image = nms(orientation, magnitude)
    # display_image(non_max_image)

    #4) Double thresholding
    _, strong_edges, weak_edges = thresh(non_max_image) #TODO: has 2 optional params, low and high. Play around with these

    #Hysteresis; follow edges to connect strong to weak edges
    hyst = hysteresis(strong_edges, weak_edges)
    final = np.dstack([hyst,hyst,hyst]).astype(np.uint8) #turn it into a 3d img of all black for easy combination with other imgs
    return final


def detect_edges_tight(img):
    np.zeros_like(img)
    rows, cols, _ = img.shape
    for x in range(rows - 1):
        for y in range(cols - 1):
            center = img[x, y]
            # above, below, left, right = 
            if not np.all(center == [255, 255, 255]):  # skip black pixels
                right = img[x, y + 1]
                bottom = img[x + 1, y]
                #check down and right pixels for changes
                if not np.all(center == right) and not np.all(center == bottom):
                    img[x, y] = [255, 255, 255]
                    # img[x, y + 1] = [255, 255, 255]
                    # img[x + 1, y] = [255, 255, 255]
                elif not np.all(center == right):
                    img[x, y] = [255, 255, 255]
                    # img[x, y + 1] = [255, 255, 255]
                elif not np.all(center == bottom):
                    img[x, y] = [255, 255, 255]
                    # img[x + 1, y] = [255, 255, 255]
                    
    return img
