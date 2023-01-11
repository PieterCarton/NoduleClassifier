# import os
# import numpy as np
# import cv2
# from PIL import Image
import file_utils

# OPENSLIDE_PATH = r'C:/openSlide/bin'
# if hasattr(os, 'add_dll_directory'):
#     # Python >= 3.8 on Windows
#     with os.add_dll_directory(OPENSLIDE_PATH):
#         import openslide
# else:
#     import openslide

# FOLDER = r"C:\Users\piete\Downloads\transfer_1899782_files_6b764aac\transfer_1793920_files_85b43f13"
# files = os.listdir(FOLDER)
# slides = list(filter(lambda f : f.endswith(".ndpi"), files))

# for slide_name in slides:
#     slide = openslide.OpenSlide(FOLDER + "\\" + slide_name)
#     img = slide.read_region((0, 0), 4, slide.level_dimensions[4])
#     img.save(f"./NoduleClassifier/output/pngs/{slide_name}.png")

results = [("A1", 0, 0, 0), ("PBS T3 1", 1, 0, 0)]
file_utils.write_results_to_excel(results, "testing", r"C:\Users\piete\Documents\results.xlsx")
