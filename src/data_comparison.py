import os
import file_utils
from slide_processing import process_slide, process_image
from PIL import Image

PROCESS_SLIDES = False

# temp path, should be chosen manually by user
DATASET_FOLDER = r".\NoduleClassifier\dataset"
files = os.listdir(DATASET_FOLDER)
slides = list(filter(lambda f : f.endswith(".ndpi"), files))
images = list(filter(lambda f : f.endswith(".JPG"), files))

# list of results from each processed slide
# should be tuple in following format:
# (name, num_s, num_m, num_l, total_area)
results = []

if PROCESS_SLIDES:
    for slide in slides:
        results.append(process_slide(DATASET_FOLDER + "\\" + slide, 4))
else:
    for image in images:
        img = Image.open(DATASET_FOLDER + "\\" + image)
        results.append(process_image(img, image))

iteration = "sizes"
file_utils.write_results_to_disk(results, f"./NoduleClassifier/output/{iteration}_contour_results.txt")