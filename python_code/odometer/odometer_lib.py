import sys
import time
sys.path.append("/home/jetson/jetson_nano/python_code/sensors")

from sensors_lib import c_speed_sensor
from sensors_lib import speed_sensor
from sensors_lib import MotorRPS
from sensors_lib import PicoRPMReader

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
        self.motor_rps = MotorRPS(29, 4)
             
    def car_motor_speed(self):
        try:
            while True:
                current_speed = self.motor_rps.get_latest_speed()
                print('car_speed_m_s: ', current_speed)
                time.sleep(0.1)  # Main thread can perform other tasks or simply wait
                return current_speed
        except KeyboardInterrupt:
            print("Program stopped by user.")
        finally:
            self.motor_rps.cleanup()

class pico_odometer:
    def __init__(self, serial_port='/dev/ttyACM0', baud_rate=115200):
        # Initialize PicoRPMReader with the specified serial port and baud rate
        self.pico_rpm_reader = PicoRPMReader(serial_port, baud_rate)
        self.pico_rpm_reader.connect()

    def get_car_speed(self):
        # This method returns the current speed of the car calculated by PicoRPMReader
        try:
            while True:
                car_speed = self.pico_rpm_reader.get_tire_speed()
                if car_speed is not None:
                    print(f'Car speed (m/s): {car_speed}')
                    return car_speed
                #time.sleep(0.1)  # Adjust the sleep time as needed
        except KeyboardInterrupt:
            print("Program stopped by user.")
