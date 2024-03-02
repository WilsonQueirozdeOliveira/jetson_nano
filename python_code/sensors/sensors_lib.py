#!/usr/bin/env python3
import os
import sys
sys.path.append("/home/jetson/jetson_nano/python_code/sensors")
from speed_sensor import RPMReader
from motor_rps_sensor import SimpleSensorRpsMotor

from pico_rpm_reader import PicoRPMReader

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
    
import time

class MotorRPS:
    def __init__(self, sensor_pin, pulses_per_revolution):
        self.rps_sensor = SimpleSensorRpsMotor(sensor_pin, pulses_per_revolution)
        self.tire_diameter_meters = 0.067
        self.tire_circumference_meters = 0.210
        self.gear_ratio = 0.6
        self.latest_rps = 0.0
        self.latest_speed = 0.0
        self.latest_speed_feedback = 0.0
        self.running = True
        self.update_thread = threading.Thread(target=self.update_rps, daemon=True)
        self.update_thread.start()

    def update_rps(self):
        while self.running:
            self.latest_rps = self.rps_sensor.read_rps()
            self.latest_speed = self.calculate_car_speed(self.latest_rps)
            time.sleep(0.1)  # Adjust sleep time as needed for update frequency

    def calculate_car_speed(self, rps):
        return (rps * self.tire_circumference_meters * self.gear_ratio)*10.0

    def get_latest_speed(self):
        return self.latest_speed
    
    def get_latest_rpm(self):
        return self.latest_rps * 60

    def get_motor_rpm(self):
        return self.get_latest_rpm() / self.gear_ratio

    def cleanup(self):
        self.running = False
        self.update_thread.join()
        self.rps_sensor.cleanup()

class RPMManager:
    def __init__(self, serial_port='/dev/ttyACM0'):
        self.rpm_reader = PicoRPMReader(serial_port=serial_port)
        self.keep_running = True

    def connect(self):
        """Establishes a connection with the serial port."""
        self.rpm_reader.connect()

    def read_tire_rpm_continuously(self):
        """Yields the tire RPM continuously."""
        try:
            while self.keep_running:
                tire_rpm = self.rpm_reader.get_tire_rpm()
                if tire_rpm:
                    yield tire_rpm
        except KeyboardInterrupt:
            print("\nProgram exited by user.")
            self.keep_running = False

    def stop(self):
        """Stops the continuous reading."""
        self.keep_running = False

