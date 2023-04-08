import http.server
import socketserver
import cv2
import numpy as np

PORT = 8000
IP_ADDRESS = "192.168.3.202"

Handler = http.server.SimpleHTTPRequestHandler

class MyHandler(Handler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()

        camera = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=2 ! video/x-raw, width=320, height=240, format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink', cv2.CAP_GSTREAMER)

        while True:
            ret, frame = camera.read()
            if not ret:
                break
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()

            self.wfile.write(b'--frame\r\n')
            self.send_header('Content-type', 'image/jpeg')
            self.send_header('Content-length', len(img_bytes))
            self.end_headers()
            self.wfile.write(img_bytes)
            self.wfile.write(b'\r\n')

        camera.release()
        return

with socketserver.TCPServer((IP_ADDRESS, PORT), MyHandler) as httpd:
    print(f"Serving at {IP_ADDRESS}:{PORT}")
    httpd.serve_forever()