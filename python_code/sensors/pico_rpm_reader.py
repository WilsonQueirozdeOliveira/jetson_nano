import serial
import math

class PicoRPMReader:
    def __init__(self, serial_port='/dev/ttyACM0', baud_rate=115200):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.ser = None
        self.gear_ratio = 3.0  # Default gear ratio
        self.tire_diameter = 0.067  # Tire diameter in meters

    def connect(self):
        """Establishes a serial connection."""
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            print(f"Connected to {self.serial_port}")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")

    def read_line(self):
        """Reads a single line from the serial port."""
        if self.ser:
            try:
                line = self.ser.readline().decode('utf-8').rstrip()
                return line
            except serial.SerialException as e:
                print(f"Error reading from serial port: {e}")
        return None

    def get_motor_rpm(self):
        """Gets the motor RPM from the serial data."""
        line = self.read_line()
        #print("self.read_line() :", line)
        if line:
            try:
                motor_rpm = float(line)
                return motor_rpm
            except ValueError:
                print("Received non-numeric data")
        return None

    def get_tire_rpm(self):
        """Calculates the tire RPM based on the motor RPM and gear ratio."""
        motor_rpm = self.get_motor_rpm()
        if motor_rpm is not None:
            return motor_rpm / self.gear_ratio
        return None

    def get_tire_speed(self):
        """Calculates and returns the tire speed in meters per second."""
        tire_rpm = self.get_tire_rpm()
        if tire_rpm is not None:
            # Convert RPM to linear speed: speed = RPM * circumference / 60
            speed = tire_rpm * (self.tire_diameter * math.pi) / 60.0
            return speed
        return None

