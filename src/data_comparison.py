import os
import file_utils
from slide_processing import process_slide, process_image
from PIL import Image

PROCESS_SLIDES = True
VALIDATION_DATA = ['A5', 'B5', 'C5', 'D5', 'PBS T3 2']

# temp path, should be chosen manually by user
DATASET_FOLDER = r"C:\Users\piete\Downloads\transfer_1899782_files_6b764aac\transfer_1793920_files_85b43f13"
files = os.listdir(DATASET_FOLDER)
slides = list(filter(lambda f : f.endswith(".ndpi"), files))
images = list(filter(lambda f : f.endswith(".JPG"), files))

print(len(slides))

for slide in slides:
    for datapoint in VALIDATION_DATA:
        if datapoint in slide:
            slides.remove(slide)

print(len(slides))

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

iteration = "no_dilation"
file_utils.write_results_to_excel(results, iteration, r"C:\Users\piete\Documents\results.xlsx")
#file_utils.write_results_to_disk(results, f"./NoduleClassifier/output/{iteration}_contour_results.txt")