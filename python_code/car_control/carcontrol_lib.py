import sys
sys.path.append("/home/jetson/jetson_nano/python_code/odometer")
sys.path.append("/home/jetson/jetson_nano/python_code/actuators")
sys.path.append("/home/jetson/jetson_nano/python_code/pid")

#from odometer_lib import c_odometer
from odometer_lib import odometer
from actuators_lib import Actuators
from pid_lib import pid

class CarControl:
    def __init__(self, steering_channel, motor_channel, wheel_sensor_pin_rear_left, wheel_sensor_pin_rear_right, wheel_diameter_m):
        self.steering_pid = pid(0, 0, 0, 1.0, 0.0, 0.0)  # initialize the steering PID controller
        self.actuators = Actuators(steering_channel, motor_channel)  # initialize the actuators
        self.output_steer = 0
        self.output_speed = 0
        self.odometer = odometer()#c_odometer()  # initialize the odometer
        self.speed_pid = pid(0, 0, 0, 2.0, 80000.0, 0.06)  # initialize the speed PID controller
        self.direction = 0
        self.speed_feedback = 0

    def set_steer(self, setpoint):
        feedback = self.output_steer
        self.output_steer = self.steering_pid.pid_update_(feedback, setpoint)  # update PID controller
        self.actuators.set_steer(self.output_steer)  # set steering angle

    def set_speed(self, setpoint):
        self.speed_feedback = self.odometer.avg_speed()#self.odometer.update_c_odometer()
        feedback = self.speed_feedback
        print('self.odometer.speed_avg: ', feedback)# get current avg_speed from c lib
        self.output_speed = self.speed_pid.pid_update_(feedback, setpoint)  # update PID controller
        print('self.output_speed: ', self.output_speed)
        
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