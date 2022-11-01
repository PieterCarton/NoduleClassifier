# Standard imports
import cv2
import numpy as np;
 
# Read image
# file_name = "./output/cutoff/cutoff300.png"
file_name = "output/cutoff/cutoff300.png"
im = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
# invert image
im = cv2.resize(im, (1000, 1000))
im = cv2.dilate(im, (5, 5), iterations=1)
im = cv2.bitwise_not(im)
# im = cv2.blur(im, (2, 2))

params = cv2.SimpleBlobDetector_Params()
print(params.filterByInertia)
print(params.minArea)

params.maxArea = 50_000
params.filterByConvexity = False
params.filterByInertia = False


# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)
 
# Detect blobs.
keypoints = detector.detect(im)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.imwrite("./output/blob_detection/dilate_and_blob_detection.png", im_with_keypoints)
cv2.waitKey(0)