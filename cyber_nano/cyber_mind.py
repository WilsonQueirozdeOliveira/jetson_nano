#!/usr/bin/env python3

import os
import time
from  GPS_VK2828U7G5LF import init_gps_GPRMC,read_gps
from mpu6050 import mpu6050
import ADS1115
import board
import busio
import Jetson.GPIO as GPIO
import sys
import cv2

sys.path.append('/opt/nvidia/jetson-gpio/lib/python')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')

from pca9685_driver import Device

servo = Device(0x40,1)

init_gps_GPRMC()
imu = mpu6050(0x68)

aceleracao_max = 0
desaceleracao_max = 0

ads = ADS1115.ADS1115()

gstreamer = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=0 ! video/x-raw, width=640, height=480, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(gstreamer)

while True:
    start = time.time()
    print("GPS:{}\n".format(read_gps()))
    print("imu")
    aceleracao_data = imu.get_accel_data()
    aceleracao_instantanea = aceleracao_data['y']
    print("aceleracao longitudinal instantanea : {:.3f} m/s^2\n".format(aceleracao_instantanea))
    if aceleracao_data['y']>aceleracao_max:
        aceleracao_max = aceleracao_data['y']
    print("aceleracao longitudinal maxima: {:.3f} m/s^2\n".format(aceleracao_max))
    if aceleracao_data['y']<desaceleracao_max:
        desaceleracao_max = aceleracao_data['y']
    print("desaceleração longitudinal maxima: {:.3f} m/s^2\n".format(desaceleracao_max))
    volt0 = 3*(ads.readADCSingleEnded()/1000)
    volt1 = (((ads.readADCSingleEnded(1)/1000)/0.185)-7.07415)*1.8
    volt2 = (((ads.readADCSingleEnded(2)/1000)/0.185)-7.1175)*2.115
    print("Tensão da bateria: {:.3f} V\n".format(volt0))
    print("Corrente do motor: {:.3} A\n".format(volt1))
    print("Corrente do computador: {:.3f} A\n".format(volt2))
    lateral = servo.get_pwm(0)
    longitudinal = servo.get_pwm(1)
    print("Controle lateral: {}\n".format(lateral))
    print("Controle longitudinal: {}\n".format(longitudinal))

    ret,frame = cam.read()
    #cv2.imshow('cam',frame)
    print("cam FPS: {}\n ".format(cam.get(cv2.CAP_PROP_FPS)))
    print("cam ret: {}\n ".format(ret))
    if cv2.waitKey(1) == ord('q'):
        break
    print("tempo de leitura dos sensores: {:0.3f} s\n".format(time.time()-start))
    time.sleep(0.5)
    os.system("clear")

cam.release()
cv2.destroyAllWindows()
