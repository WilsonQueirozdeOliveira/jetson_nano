import sys
import threading
import time
sys.path.append("/home/jetson/jetson_nano/python_code/sensors")
from pico_rpm_reader import PicoRPMReader

class RPMManager:
    def __init__(self, serial_port='/dev/ttyACM0'):
        self.rpm_reader = PicoRPMReader(serial_port=serial_port)
        self.keep_running = True
        self.tire_speed = None
        self.read_thread = None

    def connect(self):
        """Establishes a connection with the serial port."""
        self.rpm_reader.connect()

    def read_tire_speed_continuously(self):
        """Continuously updates the tire speed in meters per second in a separate thread."""
        while self.keep_running:
            try:
                self.tire_speed = self.rpm_reader.get_tire_speed()
            except KeyboardInterrupt:
                print("\nProgram exited by user.")
                self.keep_running = False

    def start_reading(self):
        """Starts the thread for continuous tire speed reading."""
        if self.read_thread is None or not self.read_thread.is_alive():
            self.read_thread = threading.Thread(target=self.read_tire_speed_continuously)
            self.read_thread.start()

    def get_current_tire_speed(self):
        """Returns the latest tire speed reading."""
        return self.tire_speed

    def stop(self):
        """Stops the continuous reading."""
        self.keep_running = False
        if self.read_thread is not None:
            self.read_thread.join()
