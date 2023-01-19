import os
import file_utils
import sys
from slide_processing import process_slide, process_image
from PIL import Image

# --- Boilerplate code for usage in shell ---
# Handle passed arguments from shell
if len(sys.argv) != 3:
    print("ERROR: missing arguments")
    print("Usage: python count_grains.py <path to folder with microscopic slides> <path to output folder>")
    exit(1)

DATASET_FOLDER = sys.argv[1]

if not os.path.isdir(DATASET_FOLDER):
    print(f"ERROR: {DATASET_FOLDER} not a valid directory")
    print("Usage: python count_grains.py <path to folder with microscopic slides> <path to output folder>")
    exit(1)

OUTPUT_FOLDER = sys.argv[2]

if not os.path.isdir(OUTPUT_FOLDER):
    print(f"ERROR: {OUTPUT_FOLDER} not a valid directory")
    print("Usage: python count_grains.py <path to folder with microscopic slides> <path to output folder>")
    exit(1)

# 
files = os.listdir(DATASET_FOLDER)
slides = list(filter(lambda f : f.endswith(".ndpi"), files))

results = []

# Main loop: process all microscopic slide inside the dataset folder
# Process the slides at level 4, which takes 1/16th of the full resolution of the microscopic image
ZOOM_LEVEL = 4
for slide in slides:
    results.append(process_slide(DATASET_FOLDER + "\\" + slide, ZOOM_LEVEL))

# Write grain counts per slide to a results file inside the output directory
file_utils.write_results_to_disk(results, f"{OUTPUT_FOLDER}/grain_count_results.txt")