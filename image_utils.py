import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from color_clustering import k_means_clustering

def setup_image(img_file_location, reduce=False):
    img = cv.imread(img_file_location, -1) #Read in file as is
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB) #swap from BGR to RGB 
    if(reduce):
        img = cv.resize(img, (720, 480), interpolation=cv.INTER_AREA)

    # gaussian = cv.GaussianBlur(img, sigma, size)
    bilateral_blurred_img = cv.bilateralFilter(img, 7, 50, 50)
    return bilateral_blurred_img


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