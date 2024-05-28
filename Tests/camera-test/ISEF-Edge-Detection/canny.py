#import of required libraries
import cv2
import numpy as np

#videocapture from camera
vid = cv2.VideoCapture(2)

#loop
while (vid.isOpened()):

    #capture frame
    ret, frame = vid.read()
    #resize frame
    frame = cv2.resize(frame, (540, 380), fx = 0, fy = 0, interpolation = cv2.INTER_CUBIC)

   # Setting parameter values 
    t_lower = 50  # Lower Threshold 
    t_upper = 150  # Upper threshold 

    # Applying the Canny Edge filter 
    edge = cv2.Canny(frame, t_lower, t_upper)

    #display video
    cv2.imshow("Live Video",frame)
    cv2.imshow('Canny', edge)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()