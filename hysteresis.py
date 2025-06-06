#File for hysteresis tracking
import numpy as np

def hysteresis(strong_edges, weak_edges):
    rows, cols, _ = strong_edges.shape
    result = strong_edges.copy() #must be init to strong bc we are only adding "weak" pixels to strong.
    
    isStrong = False
    
    thresh = 1 #how large our thresh window is
    
    for i in range(thresh, rows-thresh):
        for j in range(thresh, cols-thresh):
            
            if(weak_edges[i][j] != 0):
                #check if any of the surrounding 8 pixels are strong
                for x in range(-thresh, thresh+1):
                    for y in range(-thresh, thresh+1):
                        if(strong_edges[i+x][j+y] != 0):
                            result[i][j] = 255
                            isStrong = True
                            
                if(not isStrong):
                    result[i][j] = 0
                isStrong = False
                

    return result
