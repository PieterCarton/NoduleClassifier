import os
import numpy as np
import cv2
from PIL import Image
from image_util import cutoff


OPENSLIDE_PATH = r'C:/openSlide/bin'
if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
else:
    import openslide



# Full Pipeline
# -- 1. Open file containing slide

# Open slide using openSlide library
slide = openslide.OpenSlide(r"C:\Users\piete\Desktop\Project Minor\NoduleClassifier\dataset\slide.ndpi")

# width of pixel in micrometers
PIXEL_SIZE = float(slide.properties.get(openslide.PROPERTY_NAME_MPP_X)) * 16
PIXEL_AREA = PIXEL_SIZE * PIXEL_SIZE
# devide min area of large grain by area of pixel to get min number of pixels
LARGE_AREA = int((0.02 * 1_000_000) / PIXEL_AREA)
MEDIUM_AREA = int((0.01 * 1_000_000) / PIXEL_AREA)
SMALL_AREA = int((0.005 * 1_000_000) / PIXEL_AREA)
print(PIXEL_SIZE)
print(LARGE_AREA)
print(MEDIUM_AREA)
print(SMALL_AREA)

# level 4 should be sufficient resolution wise
# result: ~8000 x ~4500 resolution (PIL) image
img = slide.read_region((0, 0), 4, slide.level_dimensions[4])
img.show()
small = img.crop((3890, 1600, 4190, 1900))
small.save("step1.png")



# -- 2. Apply threshold to seperate dark and light regions  <------ Find optimal parameters
pixel_map = img.load()

# create new images
new_img = Image.new(img.mode, img.size)
new_pixel_map = new_img.load()

# loop through all pixels
# this part is very slow!
# maybe cpyhton or 
for x in range(img.width):
    for y in range(img.height):
        # apply threshold to each pixel
        new_pixel_map[x, y] = cutoff(pixel_map[x, y], (0, 0, 0), 300)
    if (x % int(img.height / 100) == 0):
            print(f"Thresholding: column {x} out of {img.width}")

img = new_img
img.show()
small = img.crop((3890, 1600, 4190, 1900))
small.save("step2.png")



# -- 3. Convert to openCV image
img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# -- 4. Dilate resulting image                              <------ Find optimal parameters 
img = cv2.dilate(img, np.ones((7, 7)), iterations=1)
img = cv2.bitwise_not(img)
PIL_img = Image.fromarray(img)
PIL_img.show()
small = PIL_img.crop((3890, 1600, 4190, 1900))
small.save("step3.png")



# -- 5. Apply blob detection                                <------ Find optimal parameters
params = cv2.SimpleBlobDetector_Params()

params.filterByConvexity = False
params.filterByCircularity = False
params.filterByInertia = False
params.filterByColor = True

params.filterByArea = True
params.minArea = SMALL_AREA
params.maxArea = LARGE_AREA * 256


# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)
 
# Detect blobs.
keypoints = detector.detect(img)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
PIL_img = Image.fromarray(im_with_keypoints)
PIL_img.show()
small = PIL_img.crop((3890, 1600, 4190, 1900))
small.save("step4.png")


# -- 6. Process result (display on screen or write to file)