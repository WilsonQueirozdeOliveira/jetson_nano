#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

time.sleep(1)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(15,GPIO.IN)
GPIO.setup(29,GPIO.IN)
ss1 = GPIO.input(15)
ss2 = GPIO.input(29)
print('ss1',ss1)
print('ss2',ss2)

time.sleep(0.5)
