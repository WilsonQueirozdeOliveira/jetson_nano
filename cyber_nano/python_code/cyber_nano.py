#!/usr/bin/env python3

import time
from pyPS4Controller.controller import Controller
import board
import busio
import Jetson.GPIO as GPIO
import sys

sys.path.append('/opt/nvidia/jetson-gpio/lib/python')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')

from pca9685_driver import Device

servo = Device(0x40,1)
servo.set_pwm_frequency(50)

time.sleep(0.5)

servo.set_pwm(0,330)#range 250x350

def connect():
    print("connected")
    pass

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
        print("squere pressed")

    def on_square_press(self):
        print("triangle pressed")

    def on_triangle_press(self):
        print("circle pressed")

    def on_circle_press(self):
        print("x pressed")
        i=0
        while(i<10):
            print("while")
            i= i+1        
#longitudinal control
    def on_R3_up(self, value):
        value_accelerator =  (int)(330+(value+32767)/1092)
        print("accelerator", value_accelerator)
        servo.set_pwm(1,value_accelerator)#rande 299-330-350

    def on_R3_down(self, value):
        pass
    def on_R3_y_at_rest(self):
        pass
    def on_R3_x_at_rest(self):
        pass
    def on_R3_left(self, value):
        value_reverce =  (int)(330-(value+32767)/1057)
        print("reverce",value_reverce)
        servo.set_pwm(1,value_reverce)#rande 299-330-350

    def on_R3_right(self, value):
        pass
#lateral control
    def on_L3_left(self, value):
        value_servo_left =  (int)((300+(value*-1)/655))
        print("left", value_servo_left)
        servo.set_pwm(0,value_servo_left)#range 250x350

    def on_L3_right(self, value):
        value_servo_right = (int)(300-(value/655))
        print("right", value_servo_right)
        servo.set_pwm(0,value_servo_right)#range 250x350
        
    def on_L3_up(self, value):
        pass
    def on_L3_down(self, value):
        pass
    def on_L3_y_at_rest(self):
        pass
    def on_L3_x_at_rest(self):
        print("servo", 300)
        servo.set_pwm(0,300)#range 250x350


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)

controller.listen(on_connect=connect,timeout=10)
