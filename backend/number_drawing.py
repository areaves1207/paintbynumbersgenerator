from collections import deque
import numpy as np
import cv2 as cv
from PIL import Image, ImageDraw, ImageFont
import numpy as np


#TERMINOLOGY. This has been lowkey very confusing to think about so I need to write this down for my sake
    # and for yours (thanks for reading my code lol)
# CLUSTERS - holds the k color clusters the user wanted
# CLUSTER - holds the pixel coordinates (x,y of img) that relate to the cluster
# BATCH - holds the n connected components of colors within each cluster. For example, when 
    # we have [A, A, B, A, A] as our image, our batches would be [A,A],[A,A] since they are separated
    # by the B.
def draw_numbers_cv(img, coords): #coords is where the text will be drawn
    for i, batch in enumerate(coords):
        for x, y in batch:
            cv.putText(
                    img,
                    str(i+1),
                    (y, x),
                    cv.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.25,
                    color=(255, 255, 255),
                    thickness=0,
                    lineType=cv.LINE_AA
                )
            
def draw_numbers_pil(img, coords):
    image_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(image_pil)
    font = ImageFont.truetype("DejaVuSans.ttf", 8)
    for i, batch in enumerate(coords):
        for x, y in batch:
            draw.text((y,x), str(i+1), font=font, fill=(0, 0, 0))
    return  np.array(image_pil)