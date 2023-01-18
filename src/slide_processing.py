import os
import numpy as np
import cv2
from image_util import threshold

DEFAULT_SMALL_AREA = 384

OPENSLIDE_PATH = r'C:/openSlide/bin'
if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
else:
    import openslide

def calc_area(num_small, num_medium, num_large):
    return num_small * 0.005 + num_medium * 0.01 + num_large * 0.02

def process_image(img, slide_name, LARGE_AREA=4*DEFAULT_SMALL_AREA, MEDIUM_AREA=2*DEFAULT_SMALL_AREA, SMALL_AREA=DEFAULT_SMALL_AREA):
    # -- 1. Keep copy of original image -- 
    original = img
    iteration="ggb"


    # -- 2. Apply threshold to seperate dark and light regions --
    img = threshold(original, 300)
    img.save(f"NoduleClassifier/output/{iteration}/{slide_name}_threshold.png")

    # -- 3. Convert to openCV image --
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # -- 4. Dilate resulting image --
    img = cv2.dilate(img, np.ones((7, 7)), iterations=1)
    cv2.imwrite(f"NoduleClassifier/output/{iteration}/{slide_name}_dilate.png", img)

    # -- 5. Get contours from image --
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # -----
    #ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    #img = cv2.dilate(img, np.ones((3, 3)), iterations=1)
    #cv2.imwrite(f"NoduleClassifier/output/{iteration}/{slide_name}.png", img)
    # -----

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

    # debug image
    original = cv2.cvtColor(np.array(original), cv2.COLOR_RGB2BGR)
    # original = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)
    original = cv2.drawContours(original, large_cnts, -1, (0, 0, 255), 5)
    original = cv2.drawContours(original, medium_cnts, -1, (0, 255, 255), 3)
    original = cv2.drawContours(original, small_cnts, -1, (0, 255, 0), 3)

    cv2.imwrite(f"NoduleClassifier/output/{iteration}/{slide_name}_contour.png", original)

    total_area = calc_area(len(small_cnts), len(medium_cnts), len(large_cnts))
    return (slide_name, len(small_cnts)/2, len(medium_cnts)/2, len(large_cnts)/2, total_area)



def process_slide(slide_location, level):
    # -- Open file containing slide --
    slide = openslide.OpenSlide(slide_location)

    # Get width of pixel in micrometers
    PIXEL_SIZE = float(slide.properties.get(openslide.PROPERTY_NAME_MPP_X)) * (2**level)
    PIXEL_AREA = PIXEL_SIZE * PIXEL_SIZE

    # Get minimum areas of each nodule type
    LARGE_AREA = int((0.02 * 1_000_000) / PIXEL_AREA)
    MEDIUM_AREA = int((0.01 * 1_000_000) / PIXEL_AREA)
    SMALL_AREA = int((0.005 * 1_000_000) / PIXEL_AREA)

    # Extract supplied level of slide for further processing
    img = slide.read_region((0, 0), level, slide.level_dimensions[level])
    slide_name = slide_location.split("\\")[-1]
    return process_image(img, slide_name, LARGE_AREA, MEDIUM_AREA, SMALL_AREA)

    