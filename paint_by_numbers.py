import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from color_clustering import k_means_clustering
import time
from image_setup import setup_image
import edge_detector


images = ["test_images/lemons.jpg", "test_images/1920x1080.jpg", "test_images/dali.jpeg", "test_images/dog.jpeg", "test_images/reef.jpeg", "test_images/vettriano.jpeg", "test_images/woman_in_hallway.png"]

# img = setup_image(img_file_location = images[0])

# num_colors = 16
# clustered_img = k_means_clustering(num_colors, img)
# print("TYPE:", type(clustered_img))

# np.save('my_array.npy', clustered_img)
clustered_img = np.load('my_array.npy')
# print("SHAPE", clustered_img.shape)


edges = edge_detector.detect_edges(clustered_img)
edge_detector.display_image(edges)
