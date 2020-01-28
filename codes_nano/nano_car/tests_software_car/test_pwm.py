import time

start = time.time()

import sys

sys.path.append('/usr/local/lib/python3.6/dist-packages')# caminho da biblioteca pca9685_driver
# sudo pip install PCA9685-driver(Example code for using the GPIO in Jetson Nano)
sys.path.append('/opt/nvidia/jetson-gpio/lib/python')# caminho generico sugerido
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')# caminho generico sugerido
sys.path.append('/home/nvidia/repositories/nano_gpio/gpio_env/lib/python2.7/site-packages/periphery/')# caminho generico sugerido

import Jetson.GPIO as GPIO
from pca9685_driver import Device


dev = Device(0x40,1)#endereco 0x40 , device 0,1,2,3,4,5,6 


import time

time.sleep(1)
t0=0.01
t1=0.1
#inicio

#frequencia
dev.set_pwm_frequency(50)

#seguranca
for i in range(15):
	dev.set_pwm(i, 330)

time.sleep(1)
for i in range(330,400):
	dev.set_pwm(0, i)
	time.sleep(t0)

for i in reversed(range(260,400)):
	dev.set_pwm(0, i)
	time.sleep(t0)

for i in range(260,330):
	dev.set_pwm(0, i)
	time.sleep(t0)

#motor
for i in range(330,330):
	dev.set_pwm(1, i)
	time.sleep(t1)

#seguranca
for i in range(15):
	dev.set_pwm(i, 330)

end = time.time()

print("tempo decorrido em segundos: ",end-start)

