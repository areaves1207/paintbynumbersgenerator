import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from color_clustering import k_means_clustering
import time
from image_setup import setup_image


images = ["test_images/lemons.jpg", "test_images/1920x1080.jpg", "test_images/dali.jpeg", "test_images/dog.jpeg", "test_images/reef.jpeg", "test_images/vettriano.jpeg", "test_images/woman_in_hallway.png"]

img = setup_image(img_file_location = images[0])

num_colors = 16
k_means_clustering(num_colors, img)

