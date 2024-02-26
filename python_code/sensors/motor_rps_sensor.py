import Jetson.GPIO as GPIO
import time
import threading

class SimpleSensorRpsMotor:
    def __init__(self, sensor_pin, pulses_per_revolution):
        self.sensor_pin = sensor_pin
        self.pulses_per_revolution = pulses_per_revolution
        self.rps = 0.0  # Revolutions per second
        self.last_rps = 0.0
        self.sinal_freezed = 0
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(sensor_pin, GPIO.IN)
        
        self.last_time = time.time()
        self.pulse_count = 0
        
        GPIO.add_event_detect(sensor_pin, GPIO.RISING, callback=self._pulse_detected, bouncetime=0)
        
    def _pulse_detected(self, channel):
        self.pulse_count += 1
        current_time = time.time()
        if current_time - self.last_time >= 0.1:
            self.rps = self.pulse_count / self.pulses_per_revolution
            self.pulse_count = 0
            self.last_time = current_time

    def read_rps(self):
        if self.last_rps == self.rps:
            self.sinal_freezed += 1
        else:
            self.sinal_freezed = 0
        if (self.sinal_freezed > 10) and (self.rps > 0 ):
            self.rps -= 0.1
        self.last_rps =self.rps
        return self.rps

    def cleanup(self):
        GPIO.cleanup()
