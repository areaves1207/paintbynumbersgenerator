import matplotlib.pyplot as plt
from gaussian import GaussianImage, nms, hysteresis, thresh

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
def detect_edges(img):
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
    return hyst


