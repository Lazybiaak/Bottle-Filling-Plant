import cv2

vid = cv2.VideoCapture(2)

while (vid.isOpened()):
    ret, frame=vid.read()

    cv2.imshow("live video",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()