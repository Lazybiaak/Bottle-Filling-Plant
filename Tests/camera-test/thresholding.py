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

    # conversion of BGR to grayscale is necessary to apply this operation
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # adaptive thresholding to use different threshold 
    # values on different regions of the frame.
    Thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                           cv2.THRESH_BINARY_INV, 11, 2)
 
    

    #display video
    cv2.imshow("Live Video",frame)
    cv2.imshow('Thresh Video', Thresh)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()