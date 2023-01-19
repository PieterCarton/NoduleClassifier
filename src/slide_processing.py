import os
import numpy as np
import cv2
from image_util import threshold

DEFAULT_SMALL_AREA = 384

# Minimum surface areas for each grain category in micrometers squared
MIN_SMALL_AREA = 0.005 * 1_000_000
MIN_MEDIUM_AREA = 0.01 * 1_000_000
MIN_LARGE_AREA = 0.02 * 1_000_000

# import the openslide library
OPENSLIDE_PATH = r'C:/openSlide/bin'
if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
else:
    import openslide

# calculates the total area of all grains in a slide,
# according to the methodology used in the larvae model
def calc_area(num_small, num_medium, num_large):
    return num_small * 0.005 + num_medium * 0.01 + num_large * 0.02

def process_image(img, slide_name, LARGE_AREA=4*DEFAULT_SMALL_AREA, MEDIUM_AREA=2*DEFAULT_SMALL_AREA, SMALL_AREA=DEFAULT_SMALL_AREA):
    # -- 1. Keep copy of original image -- 
    original = img

    # -- 2. Apply threshold to seperate dark and light regions --
    threshold_value = 300
    img = threshold(original, threshold_value)

    # -- 3. Convert to openCV image --
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # -- 4. Dilate resulting image --
    img = cv2.dilate(img, np.ones((7, 7)), iterations=1)

    # -- 5. Get contours from image --
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    small_cnts = []
    medium_cnts = []
    large_cnts = []

    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area > LARGE_AREA:
            large_cnts.append(cnt)
        elif area > MEDIUM_AREA:
            medium_cnts.append(cnt)
        elif area > SMALL_AREA:
            small_cnts.append(cnt)

    # convert original image to opencv format
    original = cv2.cvtColor(np.array(original), cv2.COLOR_RGB2BGR)
    # draw colour-coded large, medium and small contours
    original = cv2.drawContours(original, large_cnts, -1, (0, 0, 255), 5)
    original = cv2.drawContours(original, medium_cnts, -1, (0, 255, 255), 3)
    original = cv2.drawContours(original, small_cnts, -1, (0, 255, 0), 3)

    total_area = calc_area(len(small_cnts), len(medium_cnts), len(large_cnts))
    return (slide_name, len(small_cnts)/2, len(medium_cnts)/2, len(large_cnts)/2, total_area)



def process_slide(slide_location, level):
    """

    Args:
        slide_location (string): path to the location of a .ndpi file containing a slide.
        level (int): zoom level of the slide, where 0 is the slide at full resolution.
            Every subsequent level halves the height and with of the image.
            As the slides often have resolutions of 100k by 100k pixels, it is recomended to use a level of 4.
            Any lower level will lead to heavily increasing processing times

    Returns:
        tuple: tuple in the form (slide name, number of small grains, number of medium grains, number of large grains)
    """
    # -- Open file containing slide --
    slide = openslide.OpenSlide(slide_location)

    # Get width of pixel in micrometers
    pixel_size = float(slide.properties.get(openslide.PROPERTY_NAME_MPP_X)) * (2**level)
    # area of single pixel in micrometers squared
    pixel_area = pixel_size * pixel_size

    # Get minimum areas of each nodule type in number of pixels
    large_area = int(MIN_LARGE_AREA / pixel_area)
    medium_area = int(MIN_MEDIUM_AREA / pixel_area)
    small_area = int(MIN_SMALL_AREA / pixel_area)

    # Extract supplied level of slide for further processing
    img = slide.read_region((0, 0), level, slide.level_dimensions[level])
    # Exctract the name of the slide from the file location
    slide_name = slide_location.split("\\")[-1]

    # further process the extraced image
    return process_image(img, slide_name, large_area, medium_area, small_area)

    