import cv2
import numpy as np

# Load the image
image = cv2.imread('1.jpg')

# Convert the image from BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the range for the color red in HSV
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([180, 255, 255])

# Create masks for the red color
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = mask1 | mask2

# Bitwise-AND mask and original image
result = cv2.bitwise_and(image, image, mask=mask)

# Display the results
cv2.imshow('Original Image', image)
cv2.imshow('Red Color Detection', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
