import RPi.GPIO as GPIO
import time

class RPMReader:
    def __init__(self, pin_rear_right=15, pin_rear_left=29, sensor_pulses_per_rev=4, tire_circumference=0.2108):
        self.PIN_REAR_RIGHT = pin_rear_right
        self.PIN_REAR_LEFT = pin_rear_left
        self.SENSOR_PULSES_PER_REV = sensor_pulses_per_rev
        self.rpm_rear_right = 0
        self.rpm_rear_left = 0
        self.tire_circumference = tire_circumference  # in meters

        # Setup GPIO mode and initializations
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN_REAR_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.PIN_REAR_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Setup interrupt handlers
        GPIO.add_event_detect(self.PIN_REAR_RIGHT, GPIO.RISING, callback=self.on_rear_right_pulse, bouncetime=0)
        GPIO.add_event_detect(self.PIN_REAR_LEFT, GPIO.RISING, callback=self.on_rear_left_pulse, bouncetime=0)

    def on_rear_right_pulse(self, channel):
        self.rpm_rear_right += 1

    def on_rear_left_pulse(self, channel):
        self.rpm_rear_left += 1

    def read_rpm(self):
        rpm_rear_right = (self.rpm_rear_right * 60.0) / (self.SENSOR_PULSES_PER_REV * 2.0)
        rpm_rear_left = (self.rpm_rear_left * 60.0) / (self.SENSOR_PULSES_PER_REV * 2.0)

        self.rpm_rear_right = 0
        self.rpm_rear_left = 0

        return rpm_rear_right, rpm_rear_left

    def calculate_average_speed(self, rpm_rear_right, rpm_rear_left):
        # Calculate average RPM from both tires
        avg_rpm = (rpm_rear_right + rpm_rear_left) / 2
        print ('speed_sensor avg_rpm: ', avg_rpm)
        # Convert average RPM to m/s using the tire circumference
        meters_per_second = (avg_rpm * self.tire_circumference) / 60.0
        print ('speed_sensor m/s: ', meters_per_second)
        return meters_per_second

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        # Create RPMReader instance with a tire circumference of 0.2108 meters
        rpm_reader = RPMReader(pin_rear_right=15, pin_rear_left=29, tire_circumference=0.2108)

        while True:
            rpm_rear_right, rpm_rear_left = rpm_reader.read_rpm()
            avg_speed_combined = rpm_reader.calculate_average_speed(rpm_rear_right, rpm_rear_left)

            print("RPM Rear Right:", rpm_rear_right)
            print("RPM Rear Left:", rpm_rear_left)
            print("Average Speed Combined (m/s):", avg_speed_combined)

            #time.sleep(5)  # Delay to display RPM and speed every 5 seconds

    except KeyboardInterrupt:
        rpm_reader.cleanup()
