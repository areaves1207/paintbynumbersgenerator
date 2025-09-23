
from image_utils import display_image, setup_image_from_path
from paint_by_numbers import paint_by_numbers_gen

#python test.py
img = setup_image_from_path("./test_images/lemons.jpg", True)
img_g = paint_by_numbers_gen(img, 16, True)
display_image(img_g)