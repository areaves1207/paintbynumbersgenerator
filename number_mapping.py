from collections import deque
import numpy as np


#TERMINOLOGY. This has been lowkey very confusing to think about so I need to write this down for my sake
    # and for yours (thanks for reading my code lol)
# CLUSTERS - holds the k color clusters the user wanted
# CLUSTER - holds the pixel coordinates (x,y of img) that relate to the cluster
# BATCH - holds the n connected components of colors within each cluster. For example, when 
    # we have [A, A, B, A, A] as our image, our batches would be [A,A],[A,A] since they are separated
    # by the B.
def draw_numbers(img, clusters):
    print("HI")



def generate_batches(img, clusters, color_pallete):
    visited = np.zeros((img.shape[0], img.shape[1], 1), dtype=bool)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] #used to check up down left right easier
    batches_within_cluster = [[] for _ in range(len(clusters))]
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
            while queue:
                x,y = queue.pop()
                visited[x][y] = True
                for dx, dy in directions:
                    x, y = x + dx, y + dy
                    if 0 <= h_bound and 0 <= y < w_bound: #bounds checking
                        #if the adj pixel we are looking at is the same value as current & havent visted
                        # print("IMG",img[x][y])
                        # print("CLUSTER COLOR", cluster_color)
                        if((img[x][y] == cluster_color).all() and visited[x][y] == False):
                            queue.append((x, y))
                            batch.append((x, y))
                            
            batches_within_cluster[cluster_index].append(batch) #for cluster idx append all batches found within
    return batches_within_cluster

def center_of_mass(batches):
    for batch in batches:
        print("BATCH", batch)
        # for x in batch:
        #     print("x", x)
        #     for y in x:
        #         print("y", y)