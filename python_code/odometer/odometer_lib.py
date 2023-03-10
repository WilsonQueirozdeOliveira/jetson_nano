import sys
sys.path.insert(1, '../sensors')

import time
from sensors_lib import wheel_sensor

import threading

class odometer:
    def __init__(self, gpio_input_left, gpio_input_right, tire_diameter_m): # 15, 29, 0.067
        self.sensor_left = wheel_sensor(gpio_input_left, tire_diameter_m)
        self.sensor_right = wheel_sensor(gpio_input_right, tire_diameter_m)
        self.distance_left = 0
        self.distance_right = 0
        self.distance_total = 0
        self.speed_left = 0
        self.speed_right = 0
        self.speed_avg = 0

    def sensor_left_update(self):
        self.speed_left = self.sensor_left.speed_meters_per_second()
        print('self.speed_left: ', self.speed_left)
        self.distance_left = self.sensor_left.turn_count * 0.2104
        print('distance_left: ', self.distance_left)
        
        
    def sensor_right_update(self):
        self.speed_right = self.sensor_right.speed_meters_per_second()
        self.distance_right = self.sensor_right.turn_count * 0.2104
        print('distance_right: ', self.distance_right)

    def update(self):
        # Create two threads, one for the left sensor and one for the right sensor
        thread_left = threading.Thread(target=self.sensor_left_update)
        thread_right = threading.Thread(target=self.sensor_right_update)

        # Start both threads
        thread_left.start()
        thread_right.start()

        # Wait for both threads to finish
        thread_left.join()
        thread_right.join()

        # Update instance variables based on the sensor readings
        
        self.speed_avg = (self.speed_left + self.speed_right) / 2

        
        self.distance_total = (self.distance_left + self.distance_right) / 2
