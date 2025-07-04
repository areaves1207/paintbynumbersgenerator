import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from collections import deque


class GaussianImage:
    def __init__(self, size, sigma, img):
        self.size = size
        self.sigma = sigma
        
        self.kernel = gaussian_kernel(size, sigma)
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        smoothed_img = cv.filter2D(img, -1, self.kernel) #maybe we dont need this. Will smooth the img w/ gaussian b4 using dy dx... edit: helped reduce noise, duh
        
        # plt.imshow(img, cmap='gray')  
        # plt.show() 

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

        # print(self.orientation)
            
        
    
def gaussian_kernel(size, sigma): #NOTE: size is kernel size, sigma is how intense the filter is
    assert(size % 2 == 1) #size must be odd
    
    kernel = cv.getGaussianKernel(size, sigma)
    square_kernel = kernel @ kernel.T #turn the 1d array into a size x size matrix
    return square_kernel
    
def generate_img_gradients(img, size=3): #NOTE: RETURNS DY, DX
    dx = cv.Sobel(img, cv.CV_64F, 1, 0, ksize=size)
    dy = cv.Sobel(img, cv.CV_64F, 0, 1, ksize=size)
    return(dy, dx)
    
def get_magnitude_and_orientation(img_dy, img_dx, mag_threshold = 10):
    magnitude = np.sqrt(img_dx**2 + img_dy**2)
    magnitude[magnitude < mag_threshold] = 0 #threshold to reduce noise

    orientation_rad = np.atan2(img_dy, img_dx) #order is dy, dx
    orientation = bound_orientation(orientation_rad)

    return (magnitude, orientation)

def bound_orientation(orientation): #orientation given in radians
    orientation = orientation * 180 / np.pi #conv to angles from rads from -180 to +180
    orientation[orientation < 0] += 180 #reduce to between 0-180
    bounded_orientations = np.round(orientation / 45) * 45 #constrict all values to be 0, 45, 90, or 135
    bounded_orientations[bounded_orientations == 180] = 0 #reduce to between 0-180
    return bounded_orientations

def nms(orientation, magnitude):
    rows, cols = magnitude.shape
    nms = np.zeros_like(magnitude)

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            angle = orientation[i][j]
            # print("ANGLE:", angle)
            # print(orientation)
            curr_pixel = magnitude[i][j]

            adj_pixel1 = None
            adj_pixel2 = None
            #if neighboring pixels are BOTH greater 
            if(angle == 0):
                adj_pixel1 = magnitude[i-1][j]
                adj_pixel2 = magnitude[i+1][j]
            elif(angle == 45): 
                adj_pixel1 = magnitude[i-1][j-1]
                adj_pixel2 = magnitude[i+1][j+1]                       
            elif(angle == 90): 
                adj_pixel1 = magnitude[i][j+1]
                adj_pixel2 = magnitude[i][j-1]               
            elif(angle == 135): 
                adj_pixel1 = magnitude[i-1][j+1]
                adj_pixel2 = magnitude[i+1][j-1]                   
            else:                  
                print(f"Value not 0,45,90,135 found: {angle}", )
                assert(False)

            if(adj_pixel1 >= curr_pixel or adj_pixel2 >= curr_pixel):
                nms[i][j] = 0 #if either adj pixel is larger, set our pixel to 0
            else:
                nms[i][j] = magnitude[i][j] 
    
    return nms


def hysteresis(strong_edges, weak_edges):
    rows, cols = strong_edges.shape
    result = np.copy(strong_edges)
    visited = np.zeros_like(strong_edges, dtype=bool)
    queue = deque(zip(*np.where(strong_edges > 0)))

    while queue:
        i, j = queue.popleft()
        for x in range(-1, 2):
            for y in range(-1, 2):
                ni, nj = i + x, j + y
                if (0 <= ni < rows) and (0 <= nj < cols):
                    if weak_edges[ni, nj] and not visited[ni, nj]:
                        result[ni, nj] = 255
                        visited[ni, nj] = True
                        queue.append((ni, nj))
    return result


def thresh(gradient_magnitude_img, low_thresh=30, high_thresh=100): #typ 50-100, 100-200
    cols, rows = gradient_magnitude_img.shape
    
    strong_edges = np.zeros_like(gradient_magnitude_img)
    weak_edges = np.zeros_like(gradient_magnitude_img)

    #go thru each pixel, if higher than high, set max, if lower than low, set 0, else set middle
    for i in range(0, cols - 1):
        for j in range(0, rows - 1):
            pixel = gradient_magnitude_img[i][j]

            if(pixel >= high_thresh):
                gradient_magnitude_img[i][j] = 255
                strong_edges[i][j] = 255
            elif(pixel >= low_thresh and pixel < high_thresh):
                gradient_magnitude_img[i][j] = 100
                weak_edges[i][j] = 255
            else:
                gradient_magnitude_img[i][j] = 0
                
    return gradient_magnitude_img, strong_edges, weak_edges

