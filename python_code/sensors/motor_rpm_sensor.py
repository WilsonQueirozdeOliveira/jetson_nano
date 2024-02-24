import Jetson.GPIO as GPIO
import time
import threading

class SensorRpmMotor:
    def __init__(self, sensor_pin, pulses_per_revolution):
        self.sensor_pin = sensor_pin
        self.pulses_per_revolution = pulses_per_revolution
        self.pulse_count = 0
        self.rpm = 0
        self.lock = threading.Lock()
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN)
        
        # Add event detection for rising edge
        GPIO.add_event_detect(self.sensor_pin, GPIO.RISING, callback=self._sensor_callback)
        
        # Start a thread to calculate RPM
        self.running = True
        self.rpm_thread = threading.Thread(target=self._calculate_rpm_thread)
        self.rpm_thread.start()
    
    def _sensor_callback(self, channel):
        with self.lock:
            self.pulse_count += 1
    
    def _calculate_rpm_thread(self):
        while self.running:
            time.sleep(0.1)  # Sample rate
            with self.lock:
                # Calculate RPM
                self.rpm = (self.pulse_count / self.pulses_per_revolution) * 600
                # Reset pulse count
                self.pulse_count = 0
            
    def read_rpm(self):
        return self.rpm

    def cleanup(self):
        # Signal thread to stop
        self.running = False
        self.rpm_thread.join()
        # Clean up GPIO configuration
        GPIO.cleanup()
