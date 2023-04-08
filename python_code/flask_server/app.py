import cv2
from flask import Flask, render_template, Response, request
import time
from datetime import datetime

app = Flask(__name__)

fps_value = 0
current_clock = ""

def get_camera_stream():
    # Access the Jetson Nano CSI camera
    cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    global fps_value, current_clock
    prev_frame_time = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        frame = cv2.rotate(frame, cv2.ROTATE_180)

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_frame_time)
        prev_frame_time = current_time

        # Get current clock time
        current_clock = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Add FPS and clock text to the frame
        #cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        #cv2.putText(frame, f"Clock: {current_clock}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Update global variables for FPS and clock
        fps_value = fps
        current_clock = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(get_camera_stream(), content_type='multipart/x-mixed-replace; boundary=frame')

@app.route('/fps')
def get_fps():
    global fps_value
    return f"FPS: {fps_value:.2f}"

@app.route('/clock')
def get_clock():
    global current_clock
    return f"Clock: {current_clock}"

if __name__ == '__main__':
    app.run(host='192.168.3.202', port=5000, debug=True, threaded=True)
