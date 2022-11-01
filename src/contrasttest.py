from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from image_util import displayImage, cutoff

# --- Create window ---
root = Tk()
root.title("Contrast Test")

# --- open original image ---
file_name = r".\dataset\Grocott CIN-102 day 1 C5 40x.JPG"
img = Image.open(file_name).resize((1000, 1000))
# display original image
imgTk = ImageTk.PhotoImage(img)
displayImage("original", imgTk, 0, root)

# --- manipulate image ---
pixel_map = img.load()

# create new images
new_img = Image.new(img.mode, img.size)
new_pixel_map = new_img.load()

# loop through all pixels
for x in range(img.width):
    for y in range(img.height):
        # read color channel values of pixel
        r = pixel_map[x, y][0]
        g = pixel_map[x, y][1]
        b = pixel_map[x, y][2]

        # calculate difference with surrounding pixels
        # contrast = calc_contrast(x, y, img.width, img.height, pixel_map)
        # new_pixel_map[x, y] = (contrast, contrast, contrast)

        # !!! perform some sort of contrast detection here !!!
        new_pixel_map[x, y] = cutoff(pixel_map[x, y], (0, 0, 0), 50)
    if (x % 2 == 0):
            print(f"{x} rows")

new_img.save("./dataset/cutoff50.png")
new_imgTk = ImageTk.PhotoImage(new_img)
displayImage("edit", new_imgTk, 1, root)

# --- keep gui running ---
root.mainloop()