import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from color_clustering import k_means_clustering

def setup_image(img_file_location, size=15, sigma=(5,5), reduce=False):
    img = cv.imread(img_file_location, -1) #Read in file as is
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB) #swap from BGR to RGB 
    if(reduce):
        img = cv.resize(img, (1920, 1080), interpolation=cv.INTER_AREA)

    # gaussian = cv.GaussianBlur(img, sigma, size)
    bilateral_blurred_img = cv.bilateralFilter(img, 7, 50, 50)
    return bilateral_blurred_img