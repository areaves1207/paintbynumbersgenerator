import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from gaussian import GaussianImage


def k_means_clustering(k, img):
    #initialize our clusters and centers
    centers = pick_centers(k, img) #now we have k (x,y,z) values
    pixels = format_image(img) #now in the format RGBC, where C is the cluster the pixel is assigned to
    #Assign pixels to clusters
    


def format_image(img): #adds -1 to each pixel, so it is [RGB-1] to keep track of which cluster the pixel relates to
    formatted_img = np.array([[np.append(elem, -1) for elem in row] for row in img])
    return formatted_img #TODO: is a tad bit slow


def assign_clusters(pixels, centers):
    #assign each pixel a center cluster 
    for pixel in pixels:
        pixel[3] = get_closest_center(pixel, centers) #rgbC, C is now assigned a cluster index


# def update_clusters(pixels, centers):


    
def pick_centers(k, img): #generates k random center points that lie within the RGB space
    height, width = img.shape
    print(img)
    #pick k random centers on our image to start
    centers = []
    temp_coords = set() #holds random x and y bounded within our pixel array size
    while(len(temp_coords) != k):
        temp_coords.add((np.random.randint(width-1), np.random.randint(height-1)))
    for x,y in temp_coords:
        # print(pixels)
        centers.append(img[x][y]) #get the RGB/xyz values at that random point in the image

    return centers #we now return k cluster centers that are spawned on random points in our RGB space
    
        
        
    
def distance(p1, p2): #think of p1 having xyz coords instead of rgb :)
    diff = p1 - p2 #[R1-R2, G1-G2, B1-B2]
    return np.sqrt(np.sum(diff ** 2))


def get_closest_center(pixel, centers): #returns which center's INDEX gave min distance
    min_center_index = -1
    min_distance = float('inf')
    for center in centers:
        d = distance(pixel, center)
        if(d < min_distance):
            min_distance = d
            min_center_index = centers.index(center)

    return min_center_index



img = cv.imread("test_images/1920x1080.jpg", -1) #Read in file as is
img_height, img_width, _ = img.shape

size = 15
sigma = 5 #TODO: play around with these numbers to see what works best and not. 5,2 seems to be best
gaussian = GaussianImage(size, sigma, img) #prob want a bi-soemthing blur too. preserves edges better

num_colors = 128
k_means_clustering(100, img)



            
            