import sys
sys.path.append("/home/jetson/jetson_nano/python_code/odometer")
sys.path.append("/home/jetson/jetson_nano/python_code/actuators")
sys.path.append("/home/jetson/jetson_nano/python_code/pid")

from odometer_lib import pico_odometer
from actuators_lib import Actuators
from pid_lib import pid
import time

class CarControl:
    def __init__(self, steering_channel, motor_channel, wheel_sensor_pin_rear_left, wheel_sensor_pin_rear_right, wheel_diameter_m):
        # self.steering_pid = pid(0, 0, 0, 0.07855, 0.0, 0.00011) 
        self.steering_pid = pid(0, 0, 0, 0.9, 0.1, 0.0)  # initialize the steering PID controller
        self.actuators = Actuators(steering_channel, motor_channel)  # initialize the actuators
        self.output_steer = 0
        self.output_speed = 0
        self.pico_odom = pico_odometer()
        self.speed_pid = pid(0, 0, 0, 0.9 , 1000000.0, 8.0)  # initialize the speed PID controller
        self.direction = 0
        self.speed_feedback = 0

    def set_steer(self, setpoint):
        feedback = self.output_steer
        self.output_steer = self.steering_pid.pid_update_(feedback, setpoint)  # update PID controller
        self.actuators.set_steer(self.output_steer)  # set steering angle

    def set_speed(self, setpoint):
        self.speed_feedback = self.pico_odom.get_car_speed()
        if self.speed_feedback == None:
            print('self.pico_odom.get_car_speed() :', self.speed_feedback)
            self.speed_feedback = 20.0
            pass
        print('self.pico_odom.get_car_speed() :', self.speed_feedback)
        feedback = self.speed_feedback
        self.output_speed = self.speed_pid.pid_update_(feedback, setpoint)  # update PID controller
        
        if self.direction == "forward":
            pid_wheel_output_pwm = (self.output_speed)
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