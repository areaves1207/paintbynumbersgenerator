import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from color_clustering import k_means_clustering
import time
from image_setup import setup_image
import edge_detector
from number_mapping import draw_numbers, generate_batches

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

def quick_testing(clustered_img = None):
    if(clustered_img is not None):
        np.save('my_array.npy', clustered_img)
    return np.load('my_array.npy')
    
    
images = ["test_images/sorrento.jpg", "test_images/lemons.jpg", "test_images/1920x1080.jpg", "test_images/dali.jpeg", "test_images/dog.jpeg", "test_images/reef.jpeg", "test_images/vettriano.jpeg", "test_images/woman_in_hallway.png", "test_images/churro.jpg", "test_images/sexy_churro.jpg"]

img = setup_image(img_file_location = images[6], reduce=True)

num_colors = 4
clustered_img, labels, color_pallete = k_means_clustering(num_colors, img)

batches, center_of_masses = generate_batches(clustered_img, labels, color_pallete)

# gray = cv.cvtColor(np.array(clustered_img), cv.COLOR_RGB2GRAY)
# edgesx = cv.Canny(gray, threshold1=30, threshold2=100)

edges = edge_detector.detect_edges(clustered_img)

combined = combine_images(clustered_img.copy(), edges)
for batch in center_of_masses:
    for x, y in batch:
        combined[x][y] = [255, 255, 0]

# display_dual_imgs(clustered_img, combined)
draw_numbers(combined, center_of_masses)
edge_detector.display_image(combined)



