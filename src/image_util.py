from PIL import Image

def color_difference(pixel1, pixel2):
    """Returns the difference in color between two pixels.
    To do this, it calculates the manhattan distance between the colour values of two pixels.
    For more info, see https://en.wikipedia.org/wiki/Taxicab_geometry

    Args:
        pixel1 (tuple): tuple contain rgb values of first pixel
        pixel2 (tuple): tuple contain rgb values of secind pixel

    Returns:
        int: manhattan distance between the supplied pixels
    """
    return abs(pixel1[0] - pixel2[0]) + abs(pixel1[1] - pixel2[1])  + abs(pixel1[2] - pixel2[2])

def cutoff(pixel, target, max_difference):
    """Applies a threshold to a single pixel.
    If the distance between the supplied pixel is greate than the maximum difference, the pixel is coloured black.
    Otherwise, it is coloured white. 

    Args:
        pixel (tuple): rgb values of pixel to threshold
        target (tuple): target colour from which to measure color difference
        max_difference (int): maximum distance between the pixel and target color 
            for which the returned pixel is still coloured white

    Returns:
        tuple: color of the supplied pixel after thresholding
    """
    if (color_difference(pixel, target) <= max_difference):
        return (255, 255, 255)  # set the pixel to white if the threshold is met
    else:
        return (0, 0, 0)        # set the pixel to black otherwise

# 
def threshold(img, threshold_value):
    """Applies binary thresholding to the given image. 
    Any pixel within some distance to black will be coloured white. 
    All other pixels will be coloured black.
    See https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html for more info

    Args:
        img (PIL.Image): A PIL image on which thresholding is applied
        threshold_value (Int): Integer denoting the threshold value. 
            Any pixel that has a manhattan distance from the colour black greater than this value is coloured black. 
            All other pixels are coloured white.
    Returns:
        PIL.Image: The original supplied image with thresholding applied
    """
    # loads all pixels of the image into an array
    pixel_map = img.load()

    # create a new image, on to draw the result of thresholding
    new_img = Image.new(img.mode, img.size)
    new_pixel_map = new_img.load()

    for x in range(img.width):
        for y in range(img.height):
            # apply threshold to each pixel
            new_pixel_map[x, y] = cutoff(pixel_map[x, y], (0, 0, 0), threshold_value)
        if (x % int(img.height / 100) == 0):
                print(f"Thresholding: column {x} out of {img.width}")

    return new_img

