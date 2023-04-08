import sys
sys.path.append("/home/jetson/jetson_nano/python_code/sensors")

from sensors_lib import c_speed_sensor

class c_odometer:
    def __init__(self):
        self.c_speed_sensor = c_speed_sensor()
        
    def update_c_odometer(self):
        avg_speed = self.c_speed_sensor.avg_speed_update()
        #print("avg_speed = self.c_speed_sensor.avg_speed_update(): \n",avg_speed)
        return avg_speed
