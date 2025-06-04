import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from gaussian import GaussianImage


def k_means_clustering(k, orig_img):
    #initialize our clusters and centers
    img = format_image(orig_img) #now in the format RGBC, where C is the cluster the pixel is assigned to

    # np.savetxt("my_array.txt", img[0], delimiter=" ", fmt="%d") 

    centers, clusters = pick_centers(k, orig_img) #now we have k (x,y,z) values
    
    #Assign pixels to clusters
    assign_clusters(img, centers, clusters)
    print(img)
    

def format_image(img): #adds -1 to each pixel, so it is [RGB-1] to keep track of which cluster the pixel relates to
    formatted_img = np.array([[np.append(elem, -1) for elem in row] for row in img])
    return formatted_img #TODO: is a tad bit slow


#Assigns the fourth index of all pixels to the cluster center they are closest to
def assign_clusters(img, centers, clusters):
    #assign each pixel a center cluster 
    for row in img:
        for pixel in row:

            #Find the closest center
            min_center_index = -1
            min_distance = float('inf')
            for idx in range (len(centers)):
                center = centers[idx]
                d = distance(pixel, center) #returns distance of the cluster center
                if(d < min_distance):
                    min_distance = d
                    # print("D:",d)
                    # print("CENTERS:",centers)
                    # print("CENTER:",center)
                    min_center_index = idx

            pixel[3] = min_center_index #[R,G,B,C] where C is now assigned a cluster index


# def update_clusters(pixels, centers):
#     for 


    
def pick_centers(k, img): #generates k random center points that lie within the RGB space
    height, width, _ = img.shape
    clusters = [[] for _ in range(k)]
    #pick k random centers on our image to start
    centers = []
    temp_coords = set() #holds random x and y bounded within our pixel array size
    while(len(temp_coords) != k):
        temp_coords.add((np.random.randint(height-1), np.random.randint(width-1)))
    for x,y in temp_coords:
        # print(pixels)
        centers.append(img[x][y]) #get the RGB/xyz values at that random point in the image

    for i in range(k):
        clusters[i].append(centers[i])

    return centers, clusters #we now return k cluster centers that are spawned on random points in our RGB space
    
        
        
    
def distance(p1, p2): #think of p1 having xyz coords instead of rgb :)
    # diff = p1 - p2 #[R1-R2, G1-G2, B1-B2] (technically BGR but it doesnt matter here)
    r_diff = p1[0] - p2[0]
    g_diff = p1[1] - p2[1]
    b_diff = p1[2] - p2[2]
    return np.sqrt(r_diff**2 + g_diff**2 + b_diff**2)


img = cv.imread("test_images/1920x1080.jpg", -1) #Read in file as is
size = 15
sigma = 5 #TODO: play around with these numbers to see what works best and not. 5,2 seems to be best
gaussian = GaussianImage(size, sigma, img) #prob want a bi-soemthing blur too. preserves edges better

num_colors = 128
k_means_clustering(24, img)



            
            