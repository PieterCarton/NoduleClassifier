import numpy as np
import cv2
from PIL import Image

org = cv2.imread("step3.png")
im = cv2.imread("step3.png", cv2.IMREAD_GRAYSCALE)
im = cv2.bitwise_not(im)

cnts, _ = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# seperate into small, medium and large blobs
small = 20
medium = 100
large = 1000

small_cnts = []
medium_cnts = []
large_cnts = []

for cnt in cnts:
    area = cv2.contourArea(cnt)
    if area > large:
        large_cnts.append(cnt)
    elif area > medium:
        medium_cnts.append(cnt)
    elif area > small:
        small_cnts.append(cnt)

im = cv2.drawContours(im, large_cnts, -1, (0, 0, 255), 5)
im = cv2.drawContours(im, medium_cnts, -1, (0, 255, 255), 5)
im = cv2.drawContours(im, small_cnts, -1, (0, 255, 0), 5)

cv2.imwrite("contrours.png", im)

f = open("results.txt", "w")
f.write("ayo")
f.close()