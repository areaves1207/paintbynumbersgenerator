from collections import deque
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import time
import logging


def k_means_clustering(k, img):
    #initialize our clusters and centers
    # np.savetxt("my_array.txt", img[0], delimiter=" ", fmt="%d") 
    #centroids holds the center value, clusters holds all of the coords for each pixel and which cluster its assigned
    centroids, clusters = pick_centroids(k, img) #now we have k (x,y,z) values
    prev_centroids = None

    #Assign pixels to clusters
    print("Assigning clusters...")
    start_time = time.time()
    counter = 0 #temp to test timing stuff
    t_ac = t_uc = 0 #also temp
    while(True):
        counter += 1
        clusters, t_ac_t = assign_clusters(img, centroids, clusters)
        centroids, t_uc_t = update_centroids(img, clusters)
        t_ac += t_ac_t
        t_uc += t_uc_t #temp stuff pls delete later bro
        
        if prev_centroids is not None:
            diff = np.linalg.norm(np.array(centroids) - np.array(prev_centroids))  # total Euclidean difference
            if diff < 1e-2:
                logging.info("Minor change detected")
                break
        prev_centroids = centroids.copy()

    print("Assigning clusters completed in: ", (t_ac / counter))  
    print("Updating clusters completed in: ", (t_uc / counter))  
    #total time taken 9/20: 140s  
    
    clustered_img = np.empty_like(img)
    color_pallete = []

    start_time = time.time() 
    for i in range(k): #update each pixel to be its specified color
        coords = np.array(clusters[i], dtype=np.int32)
        clustered_img[coords[:,0], coords[:,1]] = centroids[i]
        color_pallete.append(centroids[i])
    # display_image(clustered_img, "Clustered image")

    print("Generating batches...")
    start_time = time.time()
    batches, center_of_masses = generate_batches(clustered_img, clusters, color_pallete)
    print("Batches generated in %f seconds", (time.time() - start_time)) #Time taken 9/20: 70s
    
    return clustered_img, clusters, color_pallete, batches, center_of_masses

    
#Assigns all pixels to the cluster center they are closest to
#clusters is 2d array, 1st idx is which color its associated with, 2nd idx is the pixel that belongs in that cluster
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
    return clusters, (end_time_ac - start_time_ac)


#For each cluster, find avg and return new center
def update_centroids(img, clusters):
    start_time_uc = time.time()
    img = img.astype(np.float32)

    new_centroids = []
    for cluster in clusters:
        if len(cluster) == 0: #just make sure the cluster exists. it should, but just to double check
            new_centroids.append(np.zeros(3, dtype=np.uint8))
            continue

        coords_in_cluster = np.asarray(cluster) #grab all the coords in one array ( (x1,y1), (x2,y2),...)
        pixels_array = img[coords_in_cluster[:,0], coords_in_cluster[:,1]] #arrange the pixel val at those coords
        mean = pixels_array.mean(axis=0).astype(np.uint8) #take mean, easy

        new_centroids.append(mean)

    end_time_uc = time.time()
    return new_centroids, (end_time_uc - start_time_uc)


#generates k random center points that lie within the RGB space + k empty clusters    
def pick_centroids(k, img): 
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
    
def generate_batches(img, clusters, color_pallete):
    visited = np.zeros((img.shape[0], img.shape[1], 1), dtype=bool)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] #used to check up down left right easier
    batches_within_cluster = [[] for _ in range(len(clusters))]
    center_of_mass = [[] for _ in range(len(clusters))]
    h_bound, w_bound, _ = img.shape
    
    for cluster_index, cluster in enumerate(clusters):
        #remember that cluster is an array that holds x,y values to pixels of that color
        cluster_color = color_pallete[cluster_index] #get the color value
        for coord in cluster:
            x, y = coord
            if(visited[x][y] == True): #Dont start queue if alr searched this pixel
                continue
            queue = deque()
            queue.append((x, y))
            
            #checks each cluster within the cluster
            batch = [] #holds the coords for all pixels within the specific batch in the cluster
            batch.append((x, y))
            x_center = y_center = 0
            num_pixels = 0
            while queue:
                x,y = queue.pop()
                visited[x][y] = True
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < h_bound and 0 <= ny < w_bound: #bounds checking
                        #if the adj pixel we are looking at is the same value as current & havent visted
                        # print("IMG",img[x][y])
                        # print("CLUSTER COLOR", cluster_color)
                        if((img[nx][ny] == cluster_color).all() and visited[nx][ny] == False):
                            num_pixels += 1
                            queue.append((nx, ny))
                            batch.append((nx, ny))
                            x_center += nx
                            y_center += ny
            if(num_pixels > 100): #remove tiny little bits from having numbers
                x_center_final = x_center // num_pixels
                y_center_final = y_center // num_pixels
                center_of_mass[cluster_index].append((int(x_center_final), int(y_center_final)))
                if(x_center_final < 0):
                    print(x_center, y_center, num_pixels)
            batches_within_cluster[cluster_index].append(batch) #for cluster idx append all batches found within
    return batches_within_cluster, center_of_mass