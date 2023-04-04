#!/usr/bin/env python3
#import math
#import RPi.GPIO as GPIO
#import time
import ctypes

class c_speed_sensor:
    def __init__(self):
        self.avg_speed = 0
        # Load the shared library containing the C function
        self.lib = ctypes.cdll.LoadLibrary('./c_speed_sensor.so')
        # Declare the argument and return types of the C function
        self.lib.get_speed.restype = ctypes.c_float
        
        
    def avg_speed_update(self):
        #self.lib.main()
        # Call the C function and print its return value
        
        speed = self.lib.get_speed()

        self.avg_speed = speed

        return self.avg_speed

'''
class wheel_sensor: # sensor tcrt500(KY-033)
    def __init__(self,gpio_input,tire_diameter_m):
        self.gpio_input = gpio_input
        self.tire_diameter_m = tire_diameter_m
        self.tire_perimeter_m = self.tire_diameter_m*math.pi
        #print('self.tire_perimeter_m: ',self.tire_perimeter_m)
        self.turn_time = 1
        self.turn_count = 0
        self.last_read_gpio = 0
        self.start_time = 0
        self.time_out = 0
        self.time_out_limit = 0.05
        self.time_out_return_meters_per_second = 0.0

    def speed_meters_per_second(self):
        #print('init: speed_meters_per_second')
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio_input,GPIO.IN)

        read_gpio = GPIO.input(self.gpio_input)

        self.time_out = time.time()
        while read_gpio == 1:
            read_gpio = GPIO.input(self.gpio_input)
            if (time.time()-self.time_out) > self.time_out_limit:
                return self.time_out_return_meters_per_second

        self.start_time = time.time()

        self.time_out = time.time()
        while read_gpio == 0:
            read_gpio = GPIO.input(self.gpio_input)
            if (time.time()-self.time_out) > self.time_out_limit:
                return self.time_out_return_meters_per_second

        self.time_out = time.time()
        while read_gpio == 1:
            read_gpio = GPIO.input(self.gpio_input)
            if (time.time()-self.time_out) > self.time_out_limit:
                return self.time_out_return_meters_per_second

        self.turn_time = time.time() - self.start_time
        #print('self.turn_time: ',self.turn_time)

        self.turn_count += 1
        #print('turn_count: ',self.turn_count)

        rps = 1/self.turn_time # (1 second) / turn_time
        #print('rps: ',rps)
                            
        meters_per_second = rps*self.tire_perimeter_m

        while read_gpio == 0:
            read_gpio = GPIO.input(self.gpio_input)

        GPIO.cleanup()

        return meters_per_second
'''

