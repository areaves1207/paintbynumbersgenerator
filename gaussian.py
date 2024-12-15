import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

class GaussianImage:
    def __init__(self, size, sigma, img):
        self.size = size
        self.sigma = sigma
        
        self.kernel = gaussian_kernel(size, sigma)
        smoothed_img = cv.filter2D(img, -1, self.kernel) #maybe we dont need this. Will smooth the img w/ gaussian b4 using dy dx

        self.img_dy, self.img_dx = generate_img_gradients(smoothed_img, size)
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
    
def generate_img_gradients(img, size=5): #NOTE: RETURNS DY, DX
    dx = cv.Sobel(img, cv.CV_64F, 1, 0, ksize=size)
    dy = cv.Sobel(img, cv.CV_64F, 0, 1, ksize=size)
    return (dy, dx)
    
def get_magnitude_and_orientation(img_dy, img_dx, mag_threshold = 50):
    magnitude = np.sqrt(img_dx**2 + img_dy**2)
    magnitude[magnitude < mag_threshold] = 0 #threshold to reduce noise

    orientation = np.atan2(img_dy, img_dx)
    return (magnitude, orientation)