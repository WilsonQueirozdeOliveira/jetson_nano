import cv2
import numpy as np
import time

import sys
sys.path.append("/home/jetson/jetson_nano/python_code/car_control/carcontrol_lib.py")
from carcontrol_lib import CarControl

steer_output = 0
crop = 3
count = 0

car = CarControl(0, 1, 15, 29, 0.067)  # initialize with : steering_channel, motor_channel, wheel_sensor_pin_rear_left, wheel_sensor_pin_rear_right, wheel_diameter_m

car.set_stop()
time.sleep(1)
car.set_steer(0)
time.sleep(1)
car.set_steer(100)
time.sleep(1)
car.set_steer(50)
time.sleep(1)
car.set_steer(50)
time.sleep(1)

# Define the GStreamer pipeline for camera capture at 640x480 resolution
pipeline = "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"

# Create a VideoCapture object with the GStreamer pipeline
cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Crop the frame to use only the bottom 1/4 part
    height, width, _ = frame.shape
    crop_frame = frame[:int(height / crop), :]

    # Convert the cropped frame to the HSV color space
    hsv = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for red and yellow colors in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([20, 255, 255])

    lower_yellow = np.array([24, 100, 100])
    upper_yellow = np.array([35, 255, 255])

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

    # Map the pixel counts from 0 to 100
    red_pixel_count_mapped = (red_pixel_count / (width * height / 5)) * 100
    yellow_pixel_count_mapped = (yellow_pixel_count / (width * height / 5)) * 100

    # Print the mapped pixel counts
    print(f'Red Pixels (Mapped): {red_pixel_count_mapped}')
    print(f'Yellow Pixels (Mapped): {yellow_pixel_count_mapped}')

    steer_output = int((red_pixel_count_mapped*0.8 - yellow_pixel_count_mapped)*100)

    print(f'steer output:',steer_output)

    #car.set_steer(50)

    car.set_steer(steer_output)

    # power control
    count = 0

    if count < 500:
        count += 1

        car.set_direction("forward")  # start moving forward
        car.set_speed(0.01)  # set the car speed to x m/s
        
    else:
        car.set_stop()
        car.set_stop()
        time.sleep(1)
        car.set_stop()
        time.sleep(1)

        # Exit if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            car.set_stop()
            car.set_stop()
            time.sleep(1)
            car.set_stop()
            time.sleep(1)
            break

car.set_stop()
car.set_stop()
time.sleep(1)
car.set_stop()
time.sleep(1)

# Release the camera and close OpenCV windows
cap.release()
car.set_stop()
car.set_stop()
time.sleep(1)
car.set_stop()
time.sleep(1)
cv2.destroyAllWindows()
