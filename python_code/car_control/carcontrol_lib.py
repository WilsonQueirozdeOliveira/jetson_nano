import sys
sys.path.insert(1, '../odometer')
sys.path.insert(1, '../actuators')
sys.path.insert(1, '../pid')

from odometer_lib import odometer
from odometer_lib import c_odometer
from actuators_lib import Actuators
from pid_lib import pid
import time

import threading

class CarControl:
    def __init__(self, steering_channel, motor_channel, wheel_sensor_pin_rear_left, wheel_sensor_pin_rear_right, wheel_diameter_m):
        self.steering_pid = pid(0, 0, 0, 1, 0, 0)  # initialize the steering PID controller
        self.actuators = Actuators(steering_channel, motor_channel)  # initialize the actuators
        self.output_steer = 0
        self.output_speed = 0
        self.odometer = odometer(wheel_sensor_pin_rear_left, wheel_sensor_pin_rear_right, wheel_diameter_m)  # initialize the odometer
        self.speed_pid = pid(0, 0, 0, 0.4, 8, 0)  # initialize the speed PID controller
        self.direction = 0
        #self.odometer_thread = threading.Thread(target=self._update_odometer_loop, daemon=True)
        #self.odometer_thread.start()

        self.c_odometer = c_odometer()

    #def _update_odometer_loop(self):
    #    while True:
    #        self.odometer.update()
    #        time.sleep(0.1)  # adjust update rate as needed

    def set_steer(self, setpoint):
        feedback = self.output_steer
        self.output_steer = self.steering_pid.pid_update_(feedback, setpoint)  # update PID controller
        self.actuators.set_steer(self.output_steer)  # set steering angle

    def set_speed(self, setpoint):
        #feedback = self.odometer.speed_avg  # get current speed for feedback term
        feedback = self.c_odometer.update_c_odometer()  # get current avg_speed from c lib
        print('self.odometer.speed_avg: ', self.odometer.speed_avg)
        self.output_speed = self.speed_pid.pid_update_(feedback, setpoint)  # update PID controller
        print('self.output_speed: ', self.output_speed)
        
        if self.direction == "forward":
            pid_wheel_output_pwm = 70*(self.output_speed)
            self.actuators.set_motor_forward(pid_wheel_output_pwm)  # set motor speed forward
        elif self.direction == "reverse":
            pid_wheel_output_pwm = 70*(self.output_speed)
            self.actuators.set_motor_reverse(pid_wheel_output_pwm)  # set motor speed in reverse

    def set_direction(self, direction):
        if direction == "forward":
            self.direction = "forward"
        elif direction == "reverse":
            self.direction = "reverse"

    def get_distance(self):
        return self.odometer.distance_total  # get distance traveled

    def cleanup(self):
        self.actuators.cleanup()  # clean up the actuators
        self.odometer.cleanup()  # clean up the odometer

    def set_stop(self):
        self.actuators.set_motor_forward(0)