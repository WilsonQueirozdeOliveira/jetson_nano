from pca9685_driver import Device
import time

class Actuators:
    def __init__(self, steering_channel, motor_channel):
        self.steering_channel = steering_channel
        self.motor_channel = motor_channel
        self.pwm = Device(0x40,1)  # Initialize with default I2C address (0x40) bus 1
        self.pwm.set_pwm_frequency(50)  # Set frequency to 50 Hz

    def set_motor_forward(self, power):
        if power < 0:
            power = 0
        elif power > 100:
            power = 100
        pulse_width = int(power / 100.0 * (330 - 300) + 300)
        self.pwm.set_pwm(self.motor_channel, pulse_width)
        time.sleep(1)

    def set_motor_reverse(self, power):
        if power < 0:
            power = 0
        elif power > 100:
            power = 100
        pulse_width = int(power / 100.0 * (330 - 300) + 300)
        self.pwm.set_pwm(self.motor_channel, pulse_width)
        time.sleep(1)

    def set_steer(self, position):
        if position < 0:
            position = 0
        elif position > 100:
            position = 100
        pulse_width = int(position / 100.0 * (440 - 240) + 240)
        self.pwm.set_pwm(self.steering_channel, pulse_width)
        time.sleep(1)

    def cleanup(self):
        self.pwm.cleanup()

