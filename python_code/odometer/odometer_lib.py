import sys
sys.path.append("/home/jetson/jetson_nano/python_code/sensors")

from sensors_lib import c_speed_sensor
from sensors_lib import speed_sensor
from sensors_lib import MotorRPM

class c_odometer:
    def __init__(self):
        self.c_speed_sensor = c_speed_sensor()
        
    def update_c_odometer(self):
        avg_speed = self.c_speed_sensor.avg_speed_update()
        #print("avg_speed = self.c_speed_sensor.avg_speed_update(): \n",avg_speed)
        return avg_speed

class odometer:
    def __init__(self):
        self.speed = speed_sensor()

    def avg_speed(self):
        self.speed_sensor = self.speed.calculate_average_speed()
        return self.speed_sensor
    
class motor_odometer:
    def __init__(self):
        self.motor_rpm_sensor = MotorRPM()
        self.motor_rpm_sensor.start_rpm_check(0.001)
        
    def car_motor_speed(self):
        car_speed_m_s = self.motor_rpm_sensor.get_latest_speed()
        print('car_speed_m_s: ', car_speed_m_s)
        return car_speed_m_s
