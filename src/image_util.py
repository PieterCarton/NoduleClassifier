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