import numpy as np
import matplotlib.pyplot as plt
from color_clustering import k_means_clustering
import time
from image_utils import setup_image, display_dual_imgs, combine_images
import edge_detector
from number_drawing import draw_numbers_cv, draw_numbers_pil
   
    
images = ["test_images/sorrento.jpg", "test_images/lemons.jpg", "test_images/1920x1080.jpg", "test_images/dali.jpeg", "test_images/dog.jpeg", "test_images/reef.jpeg", "test_images/vettriano.jpeg", "test_images/woman_in_hallway.png", "test_images/churro.jpg", "test_images/sexy_churro.jpg"]

img = setup_image(img_file_location = images[6], reduce=True)

num_colors = 16
clustered_img, labels, color_pallete, batches, center_of_masses = k_means_clustering(num_colors, img)

edges = edge_detector.detect_edges_canny(clustered_img)

combined = combine_images(clustered_img.copy(), edges)

final_image = draw_numbers_pil(combined, center_of_masses)
edge_detector.display_image(final_image)
