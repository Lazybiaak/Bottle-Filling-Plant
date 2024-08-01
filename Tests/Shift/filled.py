#import of required libraries
import cv2
import numpy as np
import math
image_height=700
image_width=700
# Video capture from camera
vid = cv2.VideoCapture(2)
# loop
def image_import():
    # Capture frame
    ret, frame = vid.read()
    image_height, image_width, _ = frame.shape
    image_width=int((image_width*700)/image_height)
    image_height=720
    # Resize frame
    frame = cv2.resize(frame, (image_width, image_height), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    return frame

def image_filter():
    frame=image_import()
    # Setting parameter values 
    t_lower = 50  # Lower Threshold 
    t_upper = 100  # Upper threshold 
    # Applying the Canny Edge filter 
    edge0= cv2.Canny(frame, t_lower, t_upper)
    edge= cv2.cvtColor(edge0, cv2.COLOR_GRAY2BGR)
    return edge0, edge
    
def distance():
    edge0, edge = image_filter()
    if edge0 is None or edge is None:
        return None
    x_center=int(0.50*image_width)
    y_center=int(0.225*image_height)
    first_white_pixel_above = None
    for y in range(y_center, 0, -1):
        if edge0[y, x_center] == 255:  # White pixel in the edge-detected image
            first_white_pixel_above = (x_center, y)
            break
    first_white_pixel_below = None
    for y in range(y_center, image_height):
        if edge0[y, x_center] == 255:  # White pixel in the edge-detected image
            first_white_pixel_below = (x_center, y)
            break
    value = None
    # Calculate distance between first white pixel above and first white pixel below
    if first_white_pixel_above and first_white_pixel_below:
        x1, y1 = first_white_pixel_above
        x2, y2 = first_white_pixel_below
        value = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return value

# while (1):
#     dist = distance()
#     if dist is not None:
#         print(f"Distance between first white pixel above and below: {dist:.2f} pixels")
#     else:
#         print("No white pixels detected above or below the center.")
vid.release()
cv2.destroyAllWindows()
