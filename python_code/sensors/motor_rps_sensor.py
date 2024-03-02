import Jetson.GPIO as GPIO
import time
import threading

class SimpleSensorRpsMotor:
    def __init__(self, sensor_pin, pulses_per_revolution, no_pulse_timeout=1.0):
        self.sensor_pin = sensor_pin
        self.pulses_per_revolution = pulses_per_revolution
        self.rps = 0.0  # Revolutions per second
        self.no_pulse_timeout = no_pulse_timeout  # Time in seconds to consider as no pulse detected
        self.active = True
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(sensor_pin, GPIO.IN)
        
        self.last_time = time.time()
        self.pulse_count = 0
        
        GPIO.add_event_detect(sensor_pin, GPIO.RISING, callback=self._pulse_detected, bouncetime=0)
        
        # Start the background thread to check for pulse detection
        self.check_pulse_thread = threading.Thread(target=self._check_for_pulse)
        self.check_pulse_thread.daemon = True
        self.check_pulse_thread.start()
        
    def _pulse_detected(self, channel):
        self.pulse_count += 1
        current_time = time.time()
        if current_time - self.last_time >= 0.1:
            self.rps = self.pulse_count / self.pulses_per_revolution
            self.pulse_count = 0
            self.last_time = current_time

    def _check_for_pulse(self):
        while self.active:
            time.sleep(self.no_pulse_timeout)
            if time.time() - self.last_time > self.no_pulse_timeout:
                self.rps = 0.0

    def read_rps(self):
        return self.rps

    def cleanup(self):
        self.active = False
        GPIO.cleanup()
