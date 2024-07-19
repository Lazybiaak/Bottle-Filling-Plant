import cv2
import numpy as np
from scipy import ndimage

def sobel_filters(img):
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)
    
    Ix = ndimage.convolve(img, Kx)
    Iy = ndimage.convolve(img, Ky)
    
    G = np.hypot(Ix, Iy)
    G = G / G.max() * 255
    G = G.astype(np.uint8)  # Ensure the image type is uint8
    theta = np.arctan2(Iy, Ix)
    
    return (G, theta)

def gaussian_kernel(size, sigma=1):
    size = int(size) // 2
    x, y = np.mgrid[-size:size+1, -size:size+1]
    normal = 1 / (2.0 * np.pi * sigma**2)
    g = np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
    return g

def non_max_suppression(img, D):
    M, N = img.shape
    Z = np.zeros((M, N), dtype=np.int32)
    angle = D * 180. / np.pi
    angle[angle < 0] += 180

    for i in range(1, M-1):
        for j in range(1, N-1):
            try:
                q = 255
                r = 255

                # angle 0
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    q = img[i, j+1]
                    r = img[i, j-1]
                # angle 45
                elif (22.5 <= angle[i, j] < 67.5):
                    q = img[i+1, j-1]
                    r = img[i-1, j+1]
                # angle 90
                elif (67.5 <= angle[i, j] < 112.5):
                    q = img[i+1, j]
                    r = img[i-1, j]
                # angle 135
                elif (112.5 <= angle[i, j] < 157.5):
                    q = img[i-1, j-1]
                    r = img[i+1, j+1]

                if (img[i, j] >= q) and (img[i, j] >= r):
                    Z[i, j] = img[i, j]
                else:
                    Z[i, j] = 0

            except IndexError as e:
                pass

    Z = Z.astype(np.uint8)  # Ensure the image type is uint8 for OpenCV
    return Z

# Path to .jpg file
image_path = 'images/1.jpg'
kernel_size = 5
sigma = 1.0

# Attempt to read the image file
frame = cv2.imread(image_path)

# Check if the image was successfully loaded
if frame is None:
    print(f"Error: Could not open or read the image at {image_path}")
else:
    # Resize the frame
    frame = cv2.resize(frame, (300, 300), interpolation=cv2.INTER_CUBIC)

    # Use the cvtColor() function to grayscale the image 
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    
    # Create Gaussian kernel
    kernel = gaussian_kernel(kernel_size, sigma)

    # Apply Gaussian filter
    filtered_image = cv2.filter2D(gray_image, -1, kernel)

    # Apply Sobel filter
    sobel_image, sobel_direction = sobel_filters(filtered_image)

    # Apply Non-Maximum Suppression
    suppressed_image = non_max_suppression(sobel_image, sobel_direction)

    # Display the original frame and the processed frames
    cv2.imshow("Original Image", frame)
    cv2.imshow("Gray scaled image", gray_image)
    cv2.imshow("Gaussian filtered image", filtered_image)
    cv2.imshow('Sobel Image', sobel_image)
    cv2.imshow('Suppressed Image', suppressed_image)
    
    # Wait for 'q' key to exit
    while cv2.waitKey(1) & 0xFF != ord('q'):
        pass

# Clean up
cv2.destroyAllWindows()
