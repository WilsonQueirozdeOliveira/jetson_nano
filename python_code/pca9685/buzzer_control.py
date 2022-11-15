import time
from pca9685_driver import Device

dev = Device(0x40,1)
# set the pwm frequency (Hz)
dev.set_pwm_frequency(910)# 920 max volume
while True:
    dev.set_pwm(5, 2000)# 2000 max volume
    time.sleep(1)
    dev.set_pwm(5, 0)
    time.sleep(1)

