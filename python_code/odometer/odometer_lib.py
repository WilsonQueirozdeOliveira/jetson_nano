import sys
sys.path.insert(1, '../sensors')

import time
from sensors_lib import wheel_sensor

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
        self.time_start = time.time()

    def update(self):
        time_now = time.time()
        dt = time_now - self.time_start

        self.speed_left = self.sensor_left.speed_meters_per_second()
        print('self.speed_left: ', self.speed_left)
        self.speed_right = self.sensor_right.speed_meters_per_second()
        print('self.speed_right: ', self.speed_right)
        self.speed_avg = (self.speed_left + self.speed_right) / 2

        self.distance_left += self.speed_left * dt
        self.distance_right += self.speed_right * dt
        self.distance_total = (self.distance_left + self.distance_right) / 2

        self.time_start = time_now
