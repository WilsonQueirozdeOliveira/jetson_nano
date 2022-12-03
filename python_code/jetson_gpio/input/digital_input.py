#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
GPIO.setup(15,GPIO.IN)
GPIO.setup(29,GPIO.IN)
input_1 = GPIO.input(15)
input_2 = GPIO.input(29)

count = 0
while count < 20 :
    count += 1
    time.sleep(1)
    input_1 = GPIO.input(15)
    input_2 = GPIO.input(29)
    print('count: ',count)
    print('input_1: ',input_1)
    print('input_2: ',input_2)
GPIO.cleanup()



