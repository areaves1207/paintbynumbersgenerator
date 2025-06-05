import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from color_clustering import k_means_clustering
import time


images = ["1920x1080.jpg", "dali.jpeg", "dog.jpeg", "reef.jpeg", "vettriano.jpeg", "woman_in_hallway.png"]

img = cv.imread("test_images/" + images[5], -1) #Read in file as is
img = cv.cvtColor(img, cv.COLOR_BGR2RGB) #swap from BGR to RGB 
img = cv.resize(img, (1920, 1080), interpolation=cv.INTER_AREA)

size = 15
sigma = (5,5)
gaussian = cv.GaussianBlur(img, sigma, size)
bilateral_blurred_img = cv.bilateralFilter(gaussian, 5, 50, 50)

num_colors = 16
k_means_clustering(num_colors, bilateral_blurred_img)

