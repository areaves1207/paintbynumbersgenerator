from .palette import add_padding, draw_palette_onto_img, generate_palette
from .color_clustering import k_means_clustering
from .image_utils import setup_image, display_dual_imgs, combine_images
from . import edge_detector
from .number_drawing import draw_numbers_pil
   
    
# images = ["test_images/sorrento.jpg", "test_images/lemons.jpg", "test_images/1920x1080.jpg", "test_images/dali.jpeg", "test_images/dog.jpeg", "test_images/reef.jpeg", "test_images/vettriano.jpeg", "test_images/woman_in_hallway.png", "test_images/churro.jpg", "test_images/sexy_churro.jpg"]

# img = setup_image_from_path(img_file_location = "backend/" + images[6], reduce=True)

def paint_by_numbers_gen(img, num_colors):
    img = setup_image(img, force_scale=True)
    height, width, _ = img.shape

    #TODO: potential issue i thought of it its possible when we add edges, those pixels are still
    # stored under their specific batches, so if we update with a fill in color option it
    # may color the edges too
    clustered_img, labels, color_pallete, batches, center_of_masses = k_means_clustering(num_colors, img)

    edges = edge_detector.detect_edges_canny(clustered_img.copy())
    edges_tight = edge_detector.detect_edges_tight(clustered_img.copy())

    combined = combine_images(clustered_img.copy(), edges.copy())
    combined_tight = combine_images(clustered_img.copy(), edges_tight.copy())

    numbered_image = draw_numbers_pil(combined, center_of_masses)
    numbered_image_tight = draw_numbers_pil(combined_tight, center_of_masses)

    padded_img = add_padding(numbered_image, width // 15)
    palette = generate_palette(height, color_pallete)

    padded_img_t = add_padding(numbered_image_tight, width // 15)
    final_image = draw_palette_onto_img(padded_img, palette)
    final_image_t = draw_palette_onto_img(padded_img_t, palette)

    # display_image(final_image)
    # display_dual_imgs(final_image_t, final_image)
    print("Image complete")
    return final_image_t, final_image #_t uses accurate line detector, other uses gaussian