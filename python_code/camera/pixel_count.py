import cv2
import numpy as np

# Define the GStreamer pipeline for camera capture at 640x480 resolution
pipeline = "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"

# Create a VideoCapture object with the GStreamer pipeline
cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for red and yellow colors in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # Create masks to detect red and yellow pixels
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Count the number of red and yellow pixels
    red_pixel_count = cv2.countNonZero(mask_red)
    yellow_pixel_count = cv2.countNonZero(mask_yellow)

    # Display the original frame
    #cv2.imshow('Original', frame)

    # Display the masks
    #cv2.imshow('Red Mask', mask_red)
    #cv2.imshow('Yellow Mask', mask_yellow)

    # Print the pixel counts
    print(f'Red Pixels: {red_pixel_count}')
    print(f'Yellow Pixels: {yellow_pixel_count}')

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
