#import of required libraries
import cv2
import numpy as np
import math
image_height=700
image_width=700
# Video capture from camera
# image_path = 'images/8.jpg'
vid = cv2.VideoCapture(0)
# loop
while (1):
    # Capture frame
    ret, frame = vid.read()
    # frame = cv2.imread(image_path)
    image_height, image_width, _ = frame.shape
    image_width=int((image_width*700)/image_height)
    image_height=720
    # Resize frame
    frame = cv2.resize(frame, (image_width, image_height), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    # Setting parameter values 
    t_lower = 50  # Lower Threshold 
    t_upper = 100  # Upper threshold 
    # Applying the Canny Edge filter 
    edge0= cv2.Canny(frame, t_lower, t_upper)
    edge= cv2.cvtColor(edge0, cv2.COLOR_GRAY2BGR)
    x_center=int(0.50*image_width)
    y_center=int(0.3*image_height)
    # Draw the line on the original frame
    cv2.line(edge, (0, y_center), (image_width, y_center), (0, 255, 0), 1)
    cv2.line(edge, (x_center,0), (x_center, image_height), (0, 255, 0), 1)
    # Draw the circle on the color edge-detected frame
    cv2.circle(edge, (x_center,y_center ), 2, (0, 255, 0), 4)
    first_white_pixel_above = None
    for y in range(y_center, 0, -1):
        if edge0[y, x_center] == 255:  # White pixel in the edge-detected image
            first_white_pixel_above = (x_center, y)
            cv2.line(edge, (0,y), (image_width, y), (0, 0, 255), 1)
            cv2.line(frame, (0,y), (image_width, y), (0, 0, 255), 1)
            break
    first_white_pixel_below = None
    for y in range(y_center, image_height):
        if edge0[y, x_center] == 255:  # White pixel in the edge-detected image
            first_white_pixel_below = (x_center, y)
            cv2.line(edge, (0,y), (image_width, y), (0, 0, 255), 1)
            cv2.line(frame, (0,y), (image_width, y), (0, 0, 255), 1)
            break
    # Calculate distance between first white pixel above and first white pixel below
    if first_white_pixel_above and first_white_pixel_below:
        x1, y1 = first_white_pixel_above
        x2, y2 = first_white_pixel_below
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        print(f"Distance between first white pixel above and below: {distance:.2f} pixel")
        # Display the distance on the image
        text = f"Distance: {distance:.2f} pixel"
        text_position = (10, 50)  # Position of the text
        cv2.putText(frame, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
    # Display video
    cv2.imshow("Live Video", frame)
    cv2.imshow('Canny', edge)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# vid.release()
cv2.destroyAllWindows()
