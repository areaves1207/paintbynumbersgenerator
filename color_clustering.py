import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from gaussian import GaussianImage

img = cv.imread("test_images/1920x1080.jpg", -1) #Read in file as is
img_height, img_width, color = img.shape

size = 15
sigma = 5 #TODO: play around with these numbers to see what works best and not. 5,2 seems to be best
gaussian = GaussianImage(size, sigma, img)

num_colors = 128


def k_means_clustering(k, img):
    flat_img = img.reshape(img_height, img_width, 3)
    #pick k points on our image to start
    centers = {}
    while(len(centers) != k):
        centers.add(np.random(img_width-1), np.random(img_height-1))
        
    
        
        
    
#p1 and p2 are the VALUE OF THE PIXELS, not the point in space
def distance(p1, p2):
    diff = p1 - p2 #[R1-R2, G1-G2, B1-B2]
    return np.sqrt(np.sum(diff ** 2))
    
def assign_clusters(img, cluster):
    for i in range()