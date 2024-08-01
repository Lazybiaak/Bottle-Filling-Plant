import cv2
import numpy as np
import math
import time
frames = 60  # Number of frames in the animation
delay = 100   # Delay between frames in milliseconds
# Create a white background image
image = np.ones((720, 720, 3), dtype=np.uint8) * 255

N = (255, 255, 255)
E = (100,100,100)
F = (0,100,0)
U = (0,0,200)
O = (0,0,100)
I = (0,200,0)
C = (100, 0, 0)
P = (200, 0, 0)

# Define the center and radius of the central circle
center = (360, 300)
central_radius = 100
colors = [N,N,N,N,N,N] # Light gray color in BGR
thickness = -1           # Filled circle


def rotate_station():
    for frame in range(frames):
         for i in range(num_circles):
            angle = (i * angle_step + frame * angle_step / frames) % (2 * math.pi)
            x = int(center[0] + central_radius * math.cos(angle))
            y = int(center[1] + central_radius * math.sin(angle))
            cv2.circle(image, (x, y), small_circle_radius, colors[i], thickness)  

# Draw the central circle
cv2.circle(image, center, central_radius, (200, 200, 200), thickness)

# Draw 6 circles around the edge of the central circle
num_circles = 6
angle_step = 2 * math.pi / num_circles
small_circle_radius = 30  # Radius of the smaller circles

while True:
    for i in range(num_circles):
        angle = (i+3) * angle_step
        x = int(center[0] + central_radius * math.cos(angle))
        y = int(center[1] + central_radius * math.sin(angle))
        cv2.circle(image, (x, y), small_circle_radius, colors[i], thickness)
    time.sleep(0.5)
    colors[:]=colors[-1:]+colors[:-1]

    cv2.imshow('Circle', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# rotate_station()
cv2.destroyAllWindows()
# Display the image

