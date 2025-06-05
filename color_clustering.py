import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from edge_detector import display_image
from gaussian import GaussianImage
import time

def k_means_clustering(k, img):
    #initialize our clusters and centers
    # np.savetxt("my_array.txt", img[0], delimiter=" ", fmt="%d") 
    #centroids holds the center value, clusters holds all of the coords for each pixel and which cluster its assigned
    centroids, clusters = pick_centroids(k, img) #now we have k (x,y,z) values
    prev_centroids = None

    #Assign pixels to clusters
    # for _ in range (50):
    while(True):
        clusters = assign_clusters(img, centroids, clusters)
        centroids = update_centroids(img, clusters)
        
        if prev_centroids is not None:
            diff = np.linalg.norm(np.array(centroids) - np.array(prev_centroids))  # total Euclidean difference
            if diff < 1e-4:
                print("Minor change detected")
                break
        prev_centroids = centroids.copy()
        
    
    clustered_img = np.empty_like(img)    
    for i in range(k):
        for pixel in clusters[i]:
            # print("X,Y, VAL", pixel[0], pixel[1], centroids[i])
            clustered_img[pixel[0]][pixel[1]] = centroids[i]
        
    display_image(clustered_img, "Clustered image")

    

#Assigns all pixels to the cluster center they are closest to
def assign_clusters(img, centroids, clusters):
    #assign each pixel a center cluster 
    start_time_ac = time.time()
    height, width, _ = img.shape
    centroids = np.array(centroids, dtype=np.float32)

    #this line converts our array from w,h,3 into w*h,3 which works with np's tools easier for faster functions
    easy_array = np.reshape(img, (-1, 3)).astype(np.float32) #must conv to 32 or we will overflow since cv works uint8
    distances = np.linalg.norm(easy_array[:, None, :] - centroids[None, :, :], axis=2) #calcs euclid dist fast
    cluster_indices = np.argmin(distances, axis=1) 

    #assign the closest centroid cluster for all points
    clusters = [[] for _ in range(len(centroids))]
    for idx, cluster_idx in enumerate(cluster_indices):
        x = idx // width
        y = idx % width
        clusters[cluster_idx].append((x, y))

    end_time_ac = time.time()
    print(f"Execution time of ASSIGNCLUSTERS: {end_time_ac - start_time_ac:.4f} seconds")
    return clusters


#For each cluster, find avg and return new center
def update_centroids(img, clusters):
    new_centroids = []
    for cluster in clusters:
        sum_vector = np.zeros(3, dtype=np.float32)
        for pixel in cluster:
            x=pixel[0]
            y=pixel[1]
            sum_vector += img[x][y].astype(np.float32)

        mean = (sum_vector / len(cluster)).astype(np.uint8)
        new_centroids.append(mean)

    return new_centroids



    
def pick_centroids(k, img): #generates k random center points that lie within the RGB space + k empty clusters
    height, width, _ = img.shape
    clusters = [[] for _ in range(k)]
    #pick k random centers on our image to start
    centroids = []
    temp_coords = set() #holds random x and y bounded within our pixel array size
    while(len(temp_coords) != k):
        temp_coords.add((np.random.randint(height-1), np.random.randint(width-1)))

    centroids = [img[x, y] for x, y in temp_coords] #centroid now olds xyz rgb value 0-255
    centroids = np.array(centroids, dtype=np.uint8)
    return centroids, clusters #we now return k cluster centers that are spawned on random points in our RGB space
    
        
# def distance(p1, p2): #think of p having xyz coords instead of rgb :)
#     diff = p1 - p2 #[R1-R2, G1-G2, B1-B2] (technically BGR but it doesnt matter here)
#     return np.sqrt(np.sum(diff**2))


img = cv.imread("test_images/vettriano.jpeg", -1) #Read in file as is
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img = cv.resize(img, (1920, 1080), interpolation=cv.INTER_AREA)

size = 15
sigma = (5,5) #TODO: play around with these numbers to see what works best and not. 5,2 seems to be best
gaussian = cv.GaussianBlur(img, sigma, size) #prob want a bi-soemthing blur too. preserves edges better
bilateral_blurred_img = cv.bilateralFilter(gaussian, 5, 50, 50)

num_colors = 128
start_time = time.time()

k_means_clustering(24, bilateral_blurred_img)

end_time = time.time()
print(f"Execution time: {end_time - start_time:.4f} seconds")



            
            