#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(15,GPIO.IN)
GPIO.setup(29,GPIO.IN)
input_1_left_rear_wheel = GPIO.input(15)
input_2_right_rear_wheel = GPIO.input(29)

start_time = time.time()
one_rotation_time = 0
last_input_1_left_rear_wheel = 0
count = 0
while count < 200000 :
    count += 1
    input_1_left_rear_wheel = GPIO.input(15)
    input_2_right_rear_wheel = GPIO.input(29)
    print('count: ',count)
    print('one_rotation_time: ',one_rotation_time)
    print('input_1_left_rear_wheel: ',
            input_1_left_rear_wheel)

    if last_input_1_left_rear_wheel != input_1_left_rear_wheel:
        print('########### changed ###########')
        #time.sleep(4)
        if input_1_left_rear_wheel == 0:
            print('##### input_1_left_rear_wheel == 0 #####')
            #time.sleep(4)
            one_rotation_time = time.time() - start_time 
            start_time = time.time()
    last_input_1_left_rear_wheel = input_1_left_rear_wheel

GPIO.cleanup()