from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

def displayImage(title, img, column, parent):
    # label image with title
    image_label = Label(parent, text=title)
    image_label.grid(row=0, column=column)

    image_frame = Frame(parent)
    image_frame.configure(height=1000, width=1000)
    image_frame.grid(row=1, column=column, sticky='nswe')

    # canvas to display image
    canvas = Canvas(image_frame, bg='red', scrollregion=(0, 0, img.width(), img.height()))
    canvas.create_image(0, 0, anchor=NW, image=img)

    v_scroll = Scrollbar(image_frame, orient=VERTICAL, command=canvas.yview)
    v_scroll.pack(side=RIGHT, fill=Y)

    h_scroll = Scrollbar(image_frame, orient=HORIZONTAL, command=canvas.xview)
    h_scroll.pack(side=BOTTOM, fill=X)

    canvas.configure(xscrollcommand=h_scroll.set)
    canvas.configure(yscrollcommand=v_scroll.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)


def pixel_difference(pixel1, pixel2):
    return abs(pixel1[0] - pixel2[0]) + abs(pixel1[1] - pixel2[1])  + abs(pixel1[2] - pixel2[2])

# TODO: very slow, optimize with opencv functions or NumPy
# Or: write in C using Cython?
def calc_contrast(x, y, width, height, pixel_map):
    radius = 10

    center_pixel = pixel_map[x, y]
    difference_sum = 0
    pixel_count = 0

    # sum up difference with surrounding pixels
    for i in range(x - radius, x + radius + 1, 1):
        for j in range(y - radius, y + radius + 1, 1):
            if 0 <= i < width and 0 <= j < height:
                difference_sum += pixel_difference(center_pixel, pixel_map[i, j])
                pixel_count += 1

    # calculate average difference
    return int(difference_sum / (pixel_count * 3))

def cutoff(pixel, target, max_difference):
    if (pixel_difference(pixel, target) <= max_difference):
        return (255, 255, 255)
    else:
        return (0, 0, 0)

