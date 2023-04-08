#!/usr/bin/env python3
import os
import sys
sys.path.append("/home/jetson/jetson_nano/python_code/sensors")

import ctypes

class c_speed_sensor:
    def __init__(self):
        self.avg_speed = 0
        # Load the shared library containing the C function
        
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'c_speed_sensor.so'))
        self.lib = ctypes.cdll.LoadLibrary(file_path)
        # Declare the argument and return types of the C function
        self.lib.get_speed.restype = ctypes.c_float
        self.lib.main.restype = ctypes.c_float
        
        
    def avg_speed_update(self):
        self.lib.main()
        #print("sensors_lib speed main: ",speed)
        # Call the C function and print its return value
        
        speed = self.lib.get_speed()
        #print("sensors_lib speed get: ",speed)

        return speed