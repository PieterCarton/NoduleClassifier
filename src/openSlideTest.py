# The path can also be read from a config file, etc.
OPENSLIDE_PATH = r'C:/openSlide/bin'

import os
if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
else:
    import openslide

# open slide using openSlide
slide = openslide.OpenSlide("./dataset/slide.ndpi")

# number of zoom levels
print(slide.level_count)
# size of image
print(slide.dimensions)
# width of pixel in micrometers
print(slide.properties.get("openslide.mpp-x"))

# level 4 should be sufficient resolution wise
# result: ~8000 x ~4500 resolution (PIL) image
im = slide.read_region((0, 0), 4, slide.level_dimensions[4])
print(im.size)
im.show()