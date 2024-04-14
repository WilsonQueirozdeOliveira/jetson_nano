import cv2
import numpy as np
import threading
import time
from carcontrol_lib import CarControl

# Initialize the CarControl with specific settings for channels and sensors.
car = CarControl(0, 1, 15, 29, 0.067)
car.set_stop()  # Stop the car initially.
car.set_steer(50)  # Set the steering to a neutral (straight) position.

# Shared variables across threads, protected by a lock for thread safety.
steer_output = 50  # Initial neutral steering value.
stop_thread = False  # Flag to control the stopping of the threads.
lock = threading.Lock()

def camera_steering_control():
    """Controls the steering based on the camera's input."""
    global steer_output
    # Set up the camera capture using GStreamer.
    pipeline =  "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
                #"nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)360, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    # Define HSV color range for red and yellow.
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([17, 255, 255])
    lower_yellow = np.array([24, 100, 100])
    upper_yellow = np.array([35, 255, 255])

    while not stop_thread:  # Continue until the stop flag is set.
        ret, frame = cap.read()
        if not ret:
            break  # Exit the loop if the frame is not captured correctly.

        # Process the captured frame.
        frame = frame[int(frame.shape[0] / 3):, :]  # Focus on the lower part of the frame.
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert to HSV color space.
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Update the steer_output based on the detected colors.
        with lock:
            steer_output = int(((cv2.countNonZero(mask_red) - cv2.countNonZero(mask_yellow)) / (frame.size / 5)) * 100)

    cap.release()  # Release the camera resource.
    car.set_stop()  # Stop the car when exiting the thread.

def car_speed_control():
    """Adjusts the car's speed based on the steering output."""
    
    global steer_output
    while not stop_thread:  # Continue until the stop flag is set.
        with lock:
            current_steer_output = steer_output
            car.set_direction("forward")  # start moving forward

        # Determine the speed based on the steering angle.
        if 40 <= current_steer_output <= 60:
            car.set_speed(0.8)  # Faster when going straight.
        else:
            car.set_speed(0.5)  # Slower when turning.

        car.set_steer(current_steer_output)  # Apply the steering angle.
        time.sleep(0.1)  # Short delay to reduce CPU usage.
        

    car.set_stop()  # Stop the car when exiting the thread.

def stop_all_threads():
    """Stops all threads and cleans up resources."""
    global stop_thread
    stop_thread = True  # Signal all threads to stop.
    camera_thread.join()  # Wait for the camera thread to finish.
    speed_thread.join()  # Wait for the speed thread to finish.
    car.set_stop()  # Ensure the car is completely stopped.

# Creating and starting the threads for camera steering control and car speed control.
camera_thread = threading.Thread(target=camera_steering_control)
speed_thread = threading.Thread(target=car_speed_control)

camera_thread.start()
speed_thread.start()

# The stop_all_threads() function would typically be called in response to an event (e.g., keyboard interrupt).
# Uncomment the following line to simulate stopping the threads after a delay.
time.sleep(10); stop_all_threads()  # For testing, stop threads after 10 seconds.
