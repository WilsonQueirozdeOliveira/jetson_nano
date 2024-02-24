#!/usr/bin/env python3
from sensors_lib import c_speed_sensor
from sensors_lib import MotorRPM

#speed_sensor = c_speed_sensor()
motor_rpm_sensor = MotorRPM()
motor_rpm_sensor.start_rpm_check(0.001)

while(True):
    print('...')
    #avg_speed = speed_sensor.avg_speed_update()
    #print('avg_speed: ', avg_speed)
    #motor_rpm_value = motor_rpm_sensor.start_rpm_check()
    #print('motor_rpm_value: ', motor_rpm_value)
    car_speed_m_s = motor_rpm_sensor.get_latest_speed()
    print('car_speed_m_s: ', car_speed_m_s)
    
    print('..........')

    
