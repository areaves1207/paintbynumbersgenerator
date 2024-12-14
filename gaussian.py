import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def gaussian_kernel(size, sigma): #NOTE: size is kernel size, sigma is how intense the filter is
    assert(size % 2 == 1) #size must be odd
    
    kernel = cv.getGaussianKernel(size, sigma)
    square_kernel = kernel @ kernel.T #turn the 1d array into a size x size matrix
    return square_kernel
    
def get_gaussian_derivatives(kernel, size=5):
    return (gaussian_derivative_x(kernel, size), gaussian_derivative_y(kernel, size))
    
def gaussian_derivative_x(kernel, size):
    kernel_x = cv.Sobel(kernel, cv.CV_64F, 1, 0, ksize=size)
    return kernel_x

def gaussian_derivative_y(kernel, size):
    kernel_y = cv.Sobel(kernel, cv.CV_64F, 0, 1, ksize=size)
    return kernel_y
    
def apply_gaussian_to_img(img, kernel):
    gaussian_dx, gaussian_dy = get_gaussian_derivatives(kernel, size)

    dx = cv.filter2D(img, -1, gaussian_dx)
    dy = cv.filter2D(img, -1, gaussian_dy)
    return (dx, dy)

def get_magnitude_and_orientation(dy, dx):
    magnitude = np.sqrt(dx**2 + dy**2) 
    orientation = np.atan2(dx, dy)