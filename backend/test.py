
from image_utils import display_image, setup_image_from_path
from paint_by_numbers import paint_by_numbers_gen


img = setup_image_from_path("test_images/vettriano.jpeg")
img_g = paint_by_numbers_gen(img, 24, True)
display_image(img_g[0])