from pca9685_driver import Device

# 0x40 from i2cdetect -y 1 (1 if Raspberry pi 2)
dev = Device(0x40,1)

# set the duty cycle for LED05 to 50% = 2047
dev.set_pwm(5, 4094)# max 4094 not (2**12=4096)

# set the pwm frequency (Hz)
dev.set_pwm_frequency(50)

# servo channel 0
dev.set_pwm(0, 300)