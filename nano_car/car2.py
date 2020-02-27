#!/usr/bin/env python3

import time
import os
import board #controle
import busio #controle

from approxeng.input.selectbinder import ControllerResource #controle

import sys
sys.path.append('/usr/local/lib/python3.6/dist-packages')# caminho da biblioteca pca9685_driver
# sudo pip install PCA9685-driver
sys.path.append('/opt/nvidia/jetson-gpio/lib/python')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')
sys.path.append('/home/nvidia/repositories/nano_gpio/gpio_env/lib/python2.7/site-packages/periphery/')

import Jetson.GPIO as GPIO
from pca9685_driver import Device

dev = Device(0x40,1)#endereco 0x40 , device 0,1,2,3,4,5,6 
dev.set_pwm_frequency(50)

time.sleep(0.5)

print("conecting controller....\n")
time.sleep(4)

if ControllerResource():
       ControllerConected = 1
else:
       ControllerConected = 0
       print("Controller not conected\n")
       
def main():
    while ControllerConected:

        with ControllerResource() as joystick:
            
            print("conected",type(joystick).__name__)
            time.sleep(1)

            while 1.0 > joystick['ry']:
                time.sleep(0.01)
                os.system('clear')
                print("Ctrt+c : test Out\n")
                print("Test throttle...")
                print("Press throttle",joystick['ry'])
                acelerador = joystick['ry']
            print("throttle_ok!")
            acelerador_ok = 1
            time.sleep(1)
            
            while -1.0 < joystick['rx']:
                time.sleep(0.01)
                os.system('clear')
                print("Ctrt+c : test Out\n")
                print("Test Brake...")
                print("Press Brake",joystick['rx'])
                freio = joystick['rx']
            
            print("Brake_ok!")
            freio_ok = 1
            time.sleep(1)

            print("Release Buttons")
            time.sleep(1)

            while joystick.connected:

                    time.sleep(0.05)
                    os.system('clear')
                    print("Ctrt+c : test Out")
                    
                    a = joystick['lx']
                    b = ((a*(-1))+1)/2*1
                    print("Drive",b)
                    servo = int((120*b)+(250))
                    dev.set_pwm(0,servo)
                    print("servo",servo)
                        
                    brake = joystick['rx']
                    brake = ((brake*(-1))+1)/2*0.5
                    print("brake",brake)
                        
                    throttle = joystick['ry']
                    throttle = ((throttle*(-1))+1)/2*0.5
                    print("throttle",throttle)
                    
                    print("Press Squere ",joystick['cross'])

                    signal_power = brake+throttle
                    print("signal_power",signal_power)
                    power = 330
                    if (joystick['cross']):
                        power = int((220*signal_power)+(220))
                        dev.set_pwm(1,power)               
                    else:
                        dev.set_pwm(1, 330)
                    print("power",power)

    dev.set_pwm(0, 310)
    dev.set_pwm(1, 330)

if __name__ == '__main__':
    main()