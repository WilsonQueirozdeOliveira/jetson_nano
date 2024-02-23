#!/usr/bin/env python3
import os
import sys
sys.path.append("/home/jetson/jetson_nano/python_code/sensors")
from speed_sensor import RPMReader

import threading
import ctypes

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'c_speed_sensor.so'))
lib = ctypes.cdll.LoadLibrary(file_path)
lib.main.argtypes = []

def run_main():
    lib.main()

class c_speed_sensor:
    def __init__(self):
        self.avg_speed = 0
        # Load the shared library containing the C function
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'c_speed_sensor.so'))
        self.lib = ctypes.cdll.LoadLibrary(file_path)
        # Declare the argument and return types of the C function
        self.lib.get_speed.restype = ctypes.c_float
        
        # Create and start a thread to run the C code
        main_thread = threading.Thread(target=run_main, daemon=True)
        main_thread.start()
        
    def avg_speed_update(self):
        #print("sensors_lib speed main: ",speed)
        # Call the C function and print its return value
        
        speed = self.lib.get_speed()
        #print("sensors_lib speed get: ",speed)

        return speed
    
class speed_sensor:
    def __init__(self):
        self.rpmReader = RPMReader()

    def calculate_average_speed(self):
        self.avg_speed = self.rpmReader.calculate_average_speed(self.rpmReader.read_rpm()[0],self.rpmReader.read_rpm()[1])
        return self.avg_speed