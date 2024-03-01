import serial
import time

# Replace '/dev/ttyACM0' with your Pico's serial port
serial_port = '/dev/ttyACM0'
baud_rate = 115200  # In arduino, Serial.begin(baud_rate)
try:
    with serial.Serial(serial_port, baud_rate, timeout=0) as ser:
        print("Connected to", serial_port)
        while True:
            line = ser.readline().decode('utf-8').rstrip()
            if line:  # If line is not empty
                print(line)
except serial.SerialException as e:
    print("Error opening serial port: ", e)
except KeyboardInterrupt:
    print("\nProgram exited by user.")

