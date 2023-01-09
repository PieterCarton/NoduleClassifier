import os
import file_utils
from slide_processing import process_slide

# temp path, should be chosen manually by user
DATASET_FOLDER = r"C:\Users\piete\Downloads\transfer_1899782_files_6b764aac\transfer_1793920_files_85b43f13"
files = os.listdir(DATASET_FOLDER)
slides = list(filter(lambda f : f.endswith(".ndpi"), files))

# list of results from each processed slide
# should be tuple in following format:
# (name, num_s, num_m, num_l, total_area)
results = []

for slide in slides:
    results.append(process_slide(DATASET_FOLDER + "\\" + slide, 4))

iteration = "baseline"
file_utils.write_results_to_disk(results, f"./NoduleClassifier/output/{iteration}_contour_results.txt")