from picamera import PiCamera, Color
from time import sleep

camera = PiCamera()

camera.resolution = (2592, 1900)
camera.annotate_text = "teste 2"
camera.start_preview()
sleep(5)
camera.capture('/home/test2.png')
camera.stop_preview()
