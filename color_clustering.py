import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from gaussian import GaussianImage


def k_means_clustering(k, img):
    # flat_img = img.reshape(img_height, img_width, 3) #we only need this if the img isnt formatted right. (x,y,BGR)
    # centers = pick_centers(k, img) #now we have k (x,y,z)
    
    img_copy = [subarray + [-1] for subarray in img]
    print(img_copy[0])
    #Assign colors to clusters
    






    
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
    
        
        
    
#p1 and p2 are the VALUE OF THE PIXELS, not the point in space
def distance(p1, p2): #think of p1 having xyz coords instead of rgb :)
    diff = p1 - p2 #[R1-R2, G1-G2, B1-B2]
    return np.sqrt(np.sum(diff ** 2))
    
def assign_clusters(img, cluster_centers):
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            pixel = img[x][y]



img = cv.imread("test_images/1920x1080.jpg", -1) #Read in file as is
img_height, img_width, _ = img.shape

size = 15
sigma = 5 #TODO: play around with these numbers to see what works best and not. 5,2 seems to be best
gaussian = GaussianImage(size, sigma, img) #prob want a bi-soemthing blur too. preserves edges better

num_colors = 128
print("hi")
k_means_clustering(100, img)



            
            