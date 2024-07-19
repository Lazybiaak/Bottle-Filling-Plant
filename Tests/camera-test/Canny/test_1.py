import cv2
# Path to .jpg file
image_path = 'images/1.jpg'

# Attempt to read the image file
frame = cv2.imread(image_path)

# Check if the image was successfully loaded
if frame is None:
    print(f"Error: Could not open or read the image at {image_path}")
else:
    # Resize the frame
    frame = cv2.resize(frame, (540, 380), interpolation=cv2.INTER_CUBIC)
    
    # Applying the Canny Edge filter (assuming you have defined t_lower and t_upper)
    t_lower = 100  # Example threshold values
    t_upper = 200
    edge = cv2.Canny(frame, t_lower, t_upper)
    
    # Display the original frame and the edge-detected frame
    cv2.imshow("Original Image", frame)
    cv2.imshow("Canny Edge Detection", edge)
    
    # Wait for 'q' key to exit
    while cv2.waitKey(1) & 0xFF != ord('q'):
        pass

# Clean up
cv2.destroyAllWindows()
