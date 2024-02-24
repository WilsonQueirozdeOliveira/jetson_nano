#!/usr/bin/env python3
import os
import sys
sys.path.append("/home/jetson/jetson_nano/python_code/sensors")
from speed_sensor import RPMReader
from motor_rpm_sensor import SensorRpmMotor

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
    
class MotorRPM:
    def __init__(self):
        self.rpm_sensor = SensorRpmMotor(sensor_pin=4, pulses_per_revolution=6)
        self.tire_circumference_meters = 0.067
        self.timer = None
        # Assuming a default gear ratio; this should be updated based on your specific use case
        self.gear_ratio = 1
        self.latest_rpm = 0  # Stores the latest RPM value
        self.latest_speed = 0  # Stores the latest speed value

    def start_rpm_check(self, interval=1):
        """Start periodic RPM checks with the specified interval in seconds."""
        self._schedule_rpm_check(interval)

    def _schedule_rpm_check(self, interval):
        """Schedule the next RPM check after the given interval."""
        self.timer = threading.Timer(interval, self._check_rpm, [interval])
        self.timer.start()

    def _check_rpm(self, interval):
        """Check the motor RPM and schedule the next check."""
        rpm = self.rpm_sensor.read_rpm()
        if rpm is not None:
            self.latest_rpm = rpm
            self.latest_speed = self.calculate_car_speed(rpm)
        # Schedule the next RPM check
        self._schedule_rpm_check(interval)

    def calculate_car_speed(self, rpm):
        """Calculate and return the car's speed in meters per second."""
        return (rpm * self.tire_circumference_meters * self.gear_ratio) / 60

    def set_gear_ratio(self, gear_ratio):
        """Set the current gear ratio."""
        self.gear_ratio = gear_ratio

    def get_latest_rpm(self):
        """Return the latest RPM reading."""
        return self.latest_rpm

    def get_latest_speed(self):
        """Return the latest speed calculation."""
        return self.latest_speed

    def stop_rpm_check(self):
        """Stop the periodic RPM checks."""
        if self.timer is not None:
            self.timer.cancel()

    def cleanup(self):
        """Clean up resources."""
        self.stop_rpm_check()
        self.rpm_sensor.cleanup()

