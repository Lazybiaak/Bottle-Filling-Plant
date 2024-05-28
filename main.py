import cv2
import time as time
vid = cv2.VideoCapture(2)
while(True):
	#print ("Hello World")
	ret, frame = vid.read()
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

vid.release()

cv2.destroyAllWindows()
