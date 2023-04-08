#!/usr/bin/env python3
from sensors_lib import c_speed_sensor

speed_sensor = c_speed_sensor()

while(True):
    avg_speed = speed_sensor.avg_speed_update()
    print('avg_speed: ', avg_speed)