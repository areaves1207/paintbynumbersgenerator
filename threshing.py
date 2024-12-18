#File for functions for double threshing
def thresh(gradient_magnitude_img, low_thresh=75, high_thresh=150): #typ 50-100, 100-200
    cols, rows = gradient_magnitude_img.shape

    #go thru each pixel, if higher than high, set max, if lower than low, set 0, else set middle
    for i in range(0, cols - 1):
        for j in range(0, rows - 1):
            pixel = gradient_magnitude_img[i][j]

            if(pixel >= high_thresh):
                gradient_magnitude_img[i][j] = 255
            elif(pixel >= low_thresh):
                gradient_magnitude_img[i][j] = 100
            else:
                gradient_magnitude_img[i][j] = 0
    return gradient_magnitude_img

