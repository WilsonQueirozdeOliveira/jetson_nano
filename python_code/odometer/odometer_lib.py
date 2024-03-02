import sys
import time
sys.path.append("/home/jetson/jetson_nano/python_code/sensors")
from sensors_lib import RPMManager

class pico_odometer:
    def __init__(self, serial_port='/dev/ttyACM0'):
        # Initialize RPMManager with the specified serial port
        self.rpm_manager = RPMManager(serial_port)
        self.rpm_manager.connect()
        # Start reading the tire speed in a separate thread
        self.rpm_manager.start_reading()

    def get_car_speed(self):
        # This method returns the current speed of the car as calculated by RPMManager
        try:
            car_speed = self.rpm_manager.get_current_tire_speed()
            if car_speed is not None:
                #print(f'Car speed (m/s): {car_speed}')
                return car_speed
            # Optionally, include a small delay here if necessary
            # time.sleep(0.1)
        except KeyboardInterrupt:
            print("Program stopped by user.")
