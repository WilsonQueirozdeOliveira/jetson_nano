from odometer_lib import odometer
import time

# GPIO input pins for the left and right wheels
GPIO_INPUT_LEFT = 15
GPIO_INPUT_RIGHT = 29

# Diameter of the tire in meters
TIRE_DIAMETER_M = 0.067

# Create an instance of the odometer class
my_odometer = odometer(GPIO_INPUT_LEFT, GPIO_INPUT_RIGHT, TIRE_DIAMETER_M)

# Update the odometer readings periodically
while True:
    my_odometer.update()
    print("Left distance:", my_odometer.distance_left, "meters")
    print("Right distance:", my_odometer.distance_right, "meters")
    print("Total distance:", my_odometer.distance_total, "meters")
    print("Average speed:", my_odometer.speed_avg, "meters per second")
    time.sleep(1)
