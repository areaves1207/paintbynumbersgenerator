import cv2 as cv
import numpy as np

def draw_palette(img, color_palette):
    font_size = 8
    num_colors = len(color_palette)
    width, height, _ = img.shape
    box_size = height // (num_colors*2)

    #make all white strip of img height
    palette = np.full(shape=(box_size + 1 + font_size, height, 3), fill_value=[255,255,255], dtype=np.uint8)

    for c, color_idx in enumerate(range(0, num_colors)): #loop through each color
        #the position of the top left of each square for each color:
        y = c*box_size
        top_left_point = (0, y)
        bottom_right_point = (box_size, y + box_size)
        color = tuple(int(c) for c in color_palette[color_idx])
        cv.rectangle(img = palette, pt1= top_left_point, pt2= bottom_right_point, color=color, thickness=1)
        cv.putText(img=palette, text=str(color_idx), org=(box_size, (y + box_size)//2), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,0), thickness=2)

    return palette