import RPi.GPIO as GPIO
import time

# GPIO pins for the optical sensors
PIN_REAR_RIGHT = 15
PIN_REAR_LEFT = 29

# Constants
SENSOR_PULSES_PER_REV = 20  # Number of pulses per revolution

# Variables to store the RPM for each tire
rpm_rear_right = 0
rpm_rear_left = 0

# Callback function for rear right sensor
def on_rear_right_pulse(channel):
    global rpm_rear_right
    rpm_rear_right += 1

# Callback function for rear left sensor
def on_rear_left_pulse(channel):
    global rpm_rear_left
    rpm_rear_left += 1

# Setup GPIO mode and initializations
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_REAR_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_REAR_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setup interrupt handlers
GPIO.add_event_detect(PIN_REAR_RIGHT, GPIO.RISING, callback=on_rear_right_pulse, bouncetime=20)
GPIO.add_event_detect(PIN_REAR_LEFT, GPIO.RISING, callback=on_rear_left_pulse, bouncetime=20)

try:
    while True:
        # Calculate RPM for rear right tire
        rpm_rear_right = (rpm_rear_right * 60) / (SENSOR_PULSES_PER_REV * 2)  # Calculate RPM
        print("RPM Rear Right:", rpm_rear_right)
        rpm_rear_right = 0  # Reset the RPM counter

        # Calculate RPM for rear left tire
        rpm_rear_left = (rpm_rear_left * 60) / (SENSOR_PULSES_PER_REV * 2)  # Calculate RPM
        print("RPM Rear Left:", rpm_rear_left)
        rpm_rear_left = 0  # Reset the RPM counter

        #time.sleep(5)  # Delay to display RPM every 5 seconds

except KeyboardInterrupt:
    pass

# Clean up GPIO on exit
GPIO.cleanup()

