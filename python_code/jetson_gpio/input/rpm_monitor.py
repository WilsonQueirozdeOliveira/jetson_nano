#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import os
import math


GPIO.setmode(GPIO.BOARD)
GPIO.setup(15,GPIO.IN)
GPIO.setup(29,GPIO.IN)
input_1_left_rear_wheel = GPIO.input(15)
input_2_right_rear_wheel = GPIO.input(29)

start_time = time.time()
wheel_1_turn_time = 1000
last_input_1_left_rear_wheel = 0
count = 0
tire_diameter = 0.067 # meter
tire_perimeter = tire_diameter*math.pi
second = 1
rps = 0
rpm = 0
meters_second = 0
while count < 20000 :
    os.system('cls' if os.name == 'nt' else 'clear')

    count += 1
    input_1_left_rear_wheel = GPIO.input(15)
    input_2_right_rear_wheel = GPIO.input(29)

    print('count: ',count)
    print('wheel_1_turn_time: ', wheel_1_turn_time)
    print('input_1_left_rear_wheel: ', input_1_left_rear_wheel)
    #print('tire perimeter', tire_perimeter)
    print('rps: ', rps)
    print('rpm: ', rpm)
    print('m/s: ', meters_second)
    print('mm/s: ', meters_second*1000)

    rps = second / wheel_1_turn_time

    rpm = rps*60
            
    meters_second = rps*tire_perimeter
    
    if last_input_1_left_rear_wheel != input_1_left_rear_wheel:

        if input_1_left_rear_wheel == 0:

            wheel_1_turn_time = time.time() - start_time 
            start_time = time.time()

    last_input_1_left_rear_wheel = input_1_left_rear_wheel

    if (time.time() - start_time)> 2:
        wheel_1_turn_time = 1000


GPIO.cleanup()