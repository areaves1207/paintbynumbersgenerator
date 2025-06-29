import cv2 as cv
import numpy as np

def generate_palette(img_height, color_palette):
    num_colors = len(color_palette)
    box_size = img_height // (num_colors*2 + 1)

    #make all white strip of img height
    palette = np.full(shape=(img_height, box_size * 3, 3), fill_value=[255,255,255], dtype=np.uint8)

    for c, color_idx in enumerate(range(0, num_colors), start=1): #loop through each color
        #y is the position of the TOP LEFT of each square
        y = c*box_size*2
        top_left_point = (0, y)
        bottom_right_point = (box_size // 2, y + box_size)
        color = tuple(int(c) for c in color_palette[color_idx])
        cv.rectangle(img=palette, pt1=top_left_point, pt2= bottom_right_point, color=color, thickness=-1)
        cv.putText(img=palette, text=str(color_idx+1), org=(box_size // 2, y + (box_size//2 + 1)), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0,0,0), thickness=2)

    return palette

def draw_palette_onto_img(img, palette):
    return np.concatenate((img, palette), axis=1)

def add_padding(img, padding_amt, color=[255,255,255]):
    padding = np.full(shape=(img.shape[0], padding_amt, 3), fill_value=color, dtype=np.uint8)
    padded_img = np.concatenate((img, padding), axis=1)
    return padded_img