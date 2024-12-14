import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

class GaussianImage:
    def __init__(self, size, sigma, img): #i dont like adding image here, seems coupled. TODO maybe refactor idk
        self.size = size
        self.sigma = sigma
        
        self.kernel = gaussian_kernel(size, sigma)
        # self.dx = gaussian_derivative_x(self.kernel, size)
        # self.dy = gaussian_derivative_y(self.kernel, size)
        
        self.img_dx, self.img_dy = apply_gaussian_to_img(img, self.kernel, self.size)
        self.magnitude, self.orientation = get_magnitude_and_orientation(self.img_dx, self.img_dy)
        
    def show_filtered_images(self): #chatgpt generated to display the imgs to test
        _, ax = plt.subplots(1, 4, figsize=(20, 5))
        
        # Display dx image (derivative in x direction)
        ax[0].imshow(self.img_dx, cmap='gray')
        ax[0].set_title('Filtered Image (dx)')
        ax[0].axis('off')
        
        # Display dy image (derivative in y direction)
        ax[1].imshow(self.img_dy, cmap='gray')
        ax[1].set_title('Filtered Image (dy)')
        ax[1].axis('off')
        
        # Display magnitude image
        ax[2].imshow(self.magnitude, cmap='gray')
        ax[2].set_title('Gradient Magnitude')
        ax[2].axis('off')
        
        # Display orientation image
        ax[3].imshow(self.orientation, cmap='hsv')
        ax[3].set_title('Gradient Orientation')
        ax[3].axis('off')
        
        plt.show()
            
        
    
def gaussian_kernel(size, sigma): #NOTE: size is kernel size, sigma is how intense the filter is
    assert(size % 2 == 1) #size must be odd
    
    kernel = cv.getGaussianKernel(size, sigma)
    square_kernel = kernel @ kernel.T #turn the 1d array into a size x size matrix
    return square_kernel
    
# def get_gaussian_derivatives(kernel, size=5):
#     return (gaussian_derivative_x(kernel, size), gaussian_derivative_y(kernel, size))
    
def gaussian_derivative_x(kernel, size=5):
    kernel_x = cv.Sobel(kernel, cv.CV_64F, 1, 0, ksize=size)
    return kernel_x

def gaussian_derivative_y(kernel, size=5):
    kernel_y = cv.Sobel(kernel, cv.CV_64F, 0, 1, ksize=size)
    return kernel_y
    
def apply_gaussian_to_img(img, kernel, size):
    dx = gaussian_derivative_x(kernel, size)
    dy = gaussian_derivative_y(kernel, size)

    img_dx = cv.filter2D(img, -1, dy)
    img_dy = cv.filter2D(img, -1, dx)
    return (img_dx, img_dy)

def get_magnitude_and_orientation(img_dy, img_dx):
    magnitude = np.sqrt(img_dx**2 + img_dy**2) 
    orientation = np.atan2(img_dy, img_dx)
    return (magnitude, orientation)