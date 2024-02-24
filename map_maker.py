import cv2
import numpy as np

# Load the image
image = cv2.imread('map_upscaled.png', cv2.IMREAD_GRAYSCALE)

# Apply a Gaussian blur to the image
blurred = cv2.GaussianBlur(image, (5, 5), 0)

# Use the Canny algorithm to detect edges
edges = cv2.Canny(blurred, 100, 200)

# Show the result
cv2.imshow('Edges', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()