import sys
sys.path.append("/path/to/pca9685_driver")
from carcontrol_lib import CarControl
import time
# use : sudo python3 carcontrol_lib_test.py (the speed_sensor.c file need sudo to exec)
car = CarControl(0, 1, 15, 29, 0.067)  # initialize with : steering_channel, motor_channel, wheel_sensor_pin_rear_left, wheel_sensor_pin_rear_right, wheel_diameter_m

car.set_stop()
time.sleep(1)
car.set_steer(0)
time.sleep(1)
car.set_steer(100)
time.sleep(1)
car.set_steer(50)
time.sleep(1)
car.set_steer(50)
time.sleep(1)

count = 0
while count < 300:
    count += 1
    car.set_steer(50)  # set the steering angle to 50 (0 to 100)

    car.set_direction("forward")  # start moving forward
    car.set_speed(0.062)  # set the car speed to x m/s
    
    #time.sleep(0.001)  # wait for 1 seconds

car.set_stop()
car.set_stop()
time.sleep(1)
car.set_stop()
time.sleep(1)

#distance = car.get_distance()  # get the distance traveled during the last 5 seconds
#print('distance: ', distance)
#car.cleanup()  # clean up the actuators and odometer