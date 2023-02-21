from pca9685_driver import Device
import time

class Actuators:
    def __init__(self, steering_channel, motor_channel):
        self.steering_channel = steering_channel
        self.motor_channel = motor_channel
        self.pwm = Device(0x40,1)  # Initialize with default I2C address (0x40) bus 1
        self.pwm.set_pwm_frequency(50)  # Set frequency to 50 Hz

    def set_motor_forward(self, power): #renge 350 max forward 330 stop
        if power < 0:
            power = 0
        elif power > 100:
            power = 100
        pulse_width = int(power / 100.0 * (350 - 330) + 330)
        print('pulse_width set_motor_forward :',pulse_width )
        self.pwm.set_pwm(self.motor_channel, pulse_width)

    def set_motor_reverse(self, power):# range 300 max reverser 330 stop
        self.pwm.set_pwm(self.motor_channel, 330) # reverse need a pulse to start
        time.sleep(0.1)
        self.pwm.set_pwm(self.motor_channel, 280) # reverse need a pulse to start
        time.sleep(0.2)
        self.pwm.set_pwm(self.motor_channel, 330)
        time.sleep(0.2)
        self.pwm.set_pwm(self.motor_channel, 280) # reverse need a pulse to start
        time.sleep(0.1)
        self.pwm.set_pwm(self.motor_channel, 330)
        time.sleep(0.1)
        if power < 0:
            power = 0
        elif power > 100:
            power = 100
        pulse_width = int((100 - power) / 100.0 * (330 - 300) + 300)
        self.pwm.set_pwm(self.motor_channel, pulse_width)
        print('pulse_width set_motor_reverse :',pulse_width )

    def set_steer(self, position): # steer range is 250 380
        if position < 0:
            position = 0
        elif position > 100:
            position = 100
        pulse_width = int(position / 100.0 * (380 - 250) + 250)
        self.pwm.set_pwm(self.steering_channel, pulse_width)

    def cleanup(self):
        self.pwm.cleanup()

