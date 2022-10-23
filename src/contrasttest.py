from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from image_util import displayImage 

# --- Create window ---
root = Tk()
root.title("Contrast Test")

# --- open original image ---
file_name = r"C:\Users\piete\Desktop\Project Minor\NoduleClassifier\dataset\Grocott CIN-102 day 1 C5 40x.JPG"
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

        # isolate red channel
        new_pixel_map[x, y] = (r, 0, 0)

new_imgTk = ImageTk.PhotoImage(new_img)
displayImage("edit", new_imgTk, 1, root)

# --- keep gui running ---
root.mainloop()