import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from gaussian import GaussianImage
import time

def k_means_clustering(k, img):
    #initialize our clusters and centers
    # np.savetxt("my_array.txt", img[0], delimiter=" ", fmt="%d") 

    centroids, clusters = pick_centroids(k, img) #now we have k (x,y,z) values
    #Assign pixels to clusters
    assign_clusters(img, centroids, clusters)
    centroids = update_clusters(img, clusters)    

#Assigns all pixels to the cluster center they are closest to
def assign_clusters(img, centroids, clusters):
    #assign each pixel a center cluster 
    start_time_ac = time.time()
    height, width, _ = img.shape
    for x in range(height):
        for y in range(width):
            pixel = img[x][y]

            #Find the closest center
            min_center_index = -1
            min_distance = float('inf')
            for idx in range (len(centroids)):
                center = centroids[idx]
                d = distance(pixel, center) #returns distance of the cluster center
                if(d < min_distance):
                    min_distance = d
                    min_center_index = idx

            clusters[min_center_index].append((x,y)) #add the location of the pixel to its respective cluster
    end_time_ac = time.time()
    print(f"Execution time of ASSIGNCLUSTERS: {end_time_ac - start_time_ac:.4f} seconds")


def update_clusters(img, clusters):
    new_centroids = []
    for cluster in clusters:
        sum_vector = np.zeros(3, dtype=np.float32)
        for pixel in cluster:
            sum_vector += img[pixel[0]][pixel[1]].astype(np.float32)

        mean = (sum_vector / len(cluster)).astype(np.uint8)
        new_centroids.append(mean)

    return new_centroids



    
def pick_centroids(k, img): #generates k random center points that lie within the RGB space
    height, width, _ = img.shape
    clusters = [[] for _ in range(k)]
    #pick k random centers on our image to start
    centroids = []
    temp_coords = set() #holds random x and y bounded within our pixel array size
    while(len(temp_coords) != k):
        temp_coords.add((np.random.randint(height-1), np.random.randint(width-1)))
    for x,y in temp_coords:
        # print(pixels)
        centroids.append(img[x][y]) #get the RGB/xyz values at that random point in the image

    for i in range(k):
        clusters[i].append(centroids[i])

    return centroids, clusters #we now return k cluster centers that are spawned on random points in our RGB space
    
        
def distance(p1, p2): #think of p having xyz coords instead of rgb :)
    diff = p1 - p2 #[R1-R2, G1-G2, B1-B2] (technically BGR but it doesnt matter here)
    return np.sqrt(np.sum(diff**2))


img = cv.imread("test_images/1920x1080.jpg", -1) #Read in file as is
size = 15
sigma = 5 #TODO: play around with these numbers to see what works best and not. 5,2 seems to be best
gaussian = GaussianImage(size, sigma, img) #prob want a bi-soemthing blur too. preserves edges better

num_colors = 128
start_time = time.time()

k_means_clustering(24, img)

end_time = time.time()
print(f"Execution time: {end_time - start_time:.4f} seconds")



            
            