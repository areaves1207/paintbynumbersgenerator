import numpy as np
import matplotlib.pyplot as plt
from palette import add_padding, draw_palette_onto_img, generate_palette
from color_clustering import k_means_clustering
import time
from image_utils import display_image, setup_image, display_dual_imgs, combine_images
import edge_detector
from number_drawing import draw_numbers_cv, draw_numbers_pil
   
    
images = ["test_images/sorrento.jpg", "test_images/lemons.jpg", "test_images/1920x1080.jpg", "test_images/dali.jpeg", "test_images/dog.jpeg", "test_images/reef.jpeg", "test_images/vettriano.jpeg", "test_images/woman_in_hallway.png", "test_images/churro.jpg", "test_images/sexy_churro.jpg"]

img = setup_image(img_file_location = "backend/" + images[6], reduce=True)
height, width, _ = img.shape

num_colors = 16
#TODO: potential issue i thought of it its possible when we add edges, those pixels are still
# stored under their specific batches, so if we update with a fill in color option it
# may color the edges too
clustered_img, labels, color_pallete, batches, center_of_masses = k_means_clustering(num_colors, img)

# edges = edge_detector.detect_edges_canny(clustered_img.copy())
# edges_tight = edge_detector.detect_edges_tight(clustered_img.copy())

# combined = combine_images(clustered_img.copy(), edges.copy())
# combined_tight = combine_images(clustered_img.copy(), edges_tight.copy())

# final_image = draw_numbers_pil(combined, center_of_masses)
# final_image_tight = draw_numbers_pil(combined_tight, center_of_masses)
# display_dual_imgs(final_image, final_image_tight)

padded_img = add_padding(clustered_img, width // 12)
palette = generate_palette(height, color_pallete)
final_image = draw_palette_onto_img(padded_img, palette)

display_image(final_image)