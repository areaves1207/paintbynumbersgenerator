from palette import add_padding, draw_palette_onto_img, generate_palette
from color_clustering import k_means_clustering
from image_utils import setup_image, display_dual_imgs, combine_images
import edge_detector
from number_drawing import draw_numbers_pil
import time
   
    
# images = ["test_images/sorrento.jpg", "test_images/lemons.jpg", "test_images/1920x1080.jpg", "test_images/dali.jpeg", "test_images/dog.jpeg", "test_images/reef.jpeg", "test_images/vettriano.jpeg", "test_images/woman_in_hallway.png", "test_images/churro.jpg", "test_images/sexy_churro.jpg"]

# img = setup_image_from_path(img_file_location = "backend/" + images[6], reduce=True)

def paint_by_numbers_gen(img, num_colors, force_scale = True):
    img = setup_image(img, force_scale)
    height, width, _ = img.shape

    print("k means clustering")
    start_time = time.time()
    clustered_img, labels, color_pallete, batches, center_of_masses = k_means_clustering(num_colors, img)
    print("K-means clustering finished in: %f seconds", (time.time() - start_time) ) #currently runs in ~140s

    print("edge detector")
    start_time = time.time()
    edges = edge_detector.detect_edges_canny(clustered_img.copy())
    print("Canny edge detector finished in: %f seconds", (time.time() - start_time) )
    start_time = time.time()
    # edges_tight = edge_detector.detect_edges_tight(clustered_img.copy())
    # print("Tight edge detector finished in: %f seconds", (time.time() - start_time) )
    

    print("Combining edges and photo")
    start_time = time.time()
    combined = combine_images(clustered_img.copy(), edges.copy())
    # combined_tight = combine_images(clustered_img.copy(), edges_tight.copy())
    # print("Combined edges and photos in: %f seconds", (time.time() - start_time) )

    print("Configuring numbers")
    start_time = time.time()
    numbered_image = draw_numbers_pil(combined, center_of_masses)
    # numbered_image_tight = draw_numbers_pil(combined_tight, center_of_masses)
    # print("Numbers configured in: %f seconds", (time.time() - start_time) )

    print("Creating padding, drawing pallete")
    start_time = time.time()
    padded_img = add_padding(numbered_image, width // 15)
    palette = generate_palette(height, color_pallete)
    print("Padding and pallete completed in: %f seconds", (time.time() - start_time) )

    print("Finalizing image")
    start_time = time.time()
    # padded_img_t = add_padding(numbered_image_tight, width // 15)
    final_image = draw_palette_onto_img(padded_img, palette)
    # final_image_t = draw_palette_onto_img(padded_img_t, palette)
    print("Image finalized in: %f seconds", (time.time() - start_time) )

    # display_image(final_image)
    # display_dual_imgs(final_image_t, final_image)
    print("Image complete")
    # return final_image_t, final_image #_t uses accurate line detector, other uses gaussian
    return final_image