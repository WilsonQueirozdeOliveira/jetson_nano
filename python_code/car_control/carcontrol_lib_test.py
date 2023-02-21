from carcontrol_lib import CarControl
import time

car = CarControl(0, 1, 15, 29, 6.7)  # initialize with steering channel 0, motor channel 1, wheel sensor pin 2, and wheel radius 5 cm
count = 0
while count < 200:
    count += 1
    car.set_steer(50)  # set the steering angle to 50 (0 to 100)

    car.set_direction("forward")  # start moving forward
    car.set_speed(50)  # set the car speed to x m/s
    
    time.sleep(0.1)  # wait for 1 seconds

car.set_speed(0)

distance = car.get_distance()  # get the distance traveled during the last 5 seconds
print('distance: ', distance)
#car.cleanup()  # clean up the actuators and odometer