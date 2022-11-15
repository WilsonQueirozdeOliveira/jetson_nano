import time
from pca9685_driver import Device

dev = Device(0x40,1)
# set the pwm frequency (Hz)
dev.set_pwm_frequency(910)
while True:
    # set the duty cycle for LED05 to 50% = 2047
    dev.set_pwm(5, 2000)# max 4094 not (2**12=4096)
    time.sleep(1)
    dev.set_pwm(5, 0)
    time.sleep(1)

