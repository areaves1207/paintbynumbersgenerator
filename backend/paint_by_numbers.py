from palette import add_padding, draw_palette_onto_img, generate_palette
from color_clustering import k_means_clustering
from image_utils import setup_image, desaturate, combine_images
import edge_detector
from number_drawing import draw_numbers_pil
import time
   
    
# images = ["test_images/sorrento.jpg", "test_images/lemons.jpg", "test_images/1920x1080.jpg", "test_images/dali.jpeg", "test_images/dog.jpeg", "test_images/reef.jpeg", "test_images/vettriano.jpeg", "test_images/woman_in_hallway.png", "test_images/churro.jpg", "test_images/sexy_churro.jpg"]

# img = setup_image_from_path(img_file_location = "backend/" + images[6], reduce=True)

def paint_by_numbers_gen(img, num_colors, force_scale = True):
    try:
        total_time_start = time.time()
        img = setup_image(img, force_scale)
        height, width, _ = img.shape

        print("k means clustering")
        start_time = time.time()
        clustered_img, labels, color_pallete, batches, center_of_masses = k_means_clustering(num_colors, img)
        print("K-means clustering finished in: ", (time.time() - start_time) ) #currently runs in ~140s

        print("edge detector")
        start_time = time.time()
        edges = edge_detector.detect_edges_canny(clustered_img.copy())
        print("Canny edge detector finished in: ", (time.time() - start_time) )
        start_time = time.time()
        
        print("Desaturating")
        desaturated_img = desaturate(clustered_img)

        print("Combining edges and photo")
        start_time = time.time()
        combined_desat = combine_images(desaturated_img.copy(), edges.copy())
        combined_clustered = combine_images(clustered_img.copy(), edges.copy())

        print("Configuring numbers")
        start_time = time.time()
        canvas = draw_numbers_pil(combined_desat, center_of_masses)
        numbered_clustered = draw_numbers_pil(combined_clustered, center_of_masses)

        print("Drawing palete")
        start_time = time.time()
        padded_img = add_padding(canvas, width // 15)
        palette = generate_palette(height, color_pallete)
        print("Padding and palete completed in: ", (time.time() - start_time) )

        # print("Finalizing image")
        start_time = time.time()
        combined_image = draw_palette_onto_img(padded_img, palette)

        print("Image complete. Total generation time: ",  (time.time() - total_time_start))
        return numbered_clustered, combined_image, canvas, palette
    except:
        print("Error in processing")
        return None