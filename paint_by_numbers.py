import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from color_clustering import k_means_clustering
import time
from image_setup import setup_image
import edge_detector

def display_dual_imgs(img1, img2):
    plt.subplot(1, 2, 1)
    plt.imshow(img1, cmap='gray')
    plt.axis('off')

    # Second image
    plt.subplot(1, 2, 2)
    plt.imshow(img2, cmap='gray')
    plt.axis('off')

    plt.tight_layout()
    plt.show()
    
def combine_images(img, edges):
    img[edges == 255] = 0
    return img
    
    
images = ["test_images/lemons.jpg", "test_images/1920x1080.jpg", "test_images/dali.jpeg", "test_images/dog.jpeg", "test_images/reef.jpeg", "test_images/vettriano.jpeg", "test_images/woman_in_hallway.png"]

# img = setup_image(img_file_location = images[0])

# num_colors = 16
# clustered_img = k_means_clustering(num_colors, img)
# print("TYPE:", type(clustered_img))

# np.save('my_array.npy', clustered_img)
clustered_img = np.load('my_array.npy')

gray = cv.cvtColor(np.array(clustered_img), cv.COLOR_RGB2GRAY)
# edgesx = cv.Canny(gray, threshold1=30, threshold2=100)

edges = edge_detector.detect_edges(clustered_img)

combined = combine_images(clustered_img.copy(), edges)


# edge_detector.display_image(combined)
display_dual_imgs(clustered_img, combined)



