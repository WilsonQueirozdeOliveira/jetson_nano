import time
import os
import board #controle
import busio #controle

from approxeng.input.selectbinder import ControllerResource #controle

import sys
sys.path.append('/usr/local/lib/python3.6/dist-packages')# caminho da biblioteca pca9685_driver
# sudo pip install PCA9685-driver
sys.path.append('/opt/nvidia/jetson-gpio/lib/python')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')
sys.path.append('/home/nvidia/repositories/nano_gpio/gpio_env/lib/python2.7/site-packages/periphery/')

import Jetson.GPIO as GPIO
from pca9685_driver import Device

dev = Device(0x40,1)#endereco 0x40 , device 0,1,2,3,4,5,6 
dev.set_pwm_frequency(50)

time.sleep(0.5)

while True:

       with ControllerResource() as joystick:
          
           print("conectado",type(joystick).__name__)
           time.sleep(1)

           while 1.0 > joystick['ry']:
               time.sleep(0.1)
               os.system('clear')
               print("Ctrt+c : Sair do Teste\n")
               print("Calibrar Acelerador...")
               print("Acione Acelerador",joystick['ry'])
               acelerador = joystick['ry']
           print("acelerador_ok!")
           acelerador_ok = 1
           time.sleep(1)
           
           while -1.0 < joystick['rx']:
               time.sleep(0.1)
               os.system('clear')
               print("Ctrt+c : Sair do Teste\n")
               print("Calibrar Freio...")
               print("Acione Freio",joystick['rx'])
               freio = joystick['rx']
        
           print("freio_ok!")
           freio_ok = 1
           time.sleep(1)

           print("Liberar Controles")
           time.sleep(2)

           while joystick.connected:

                time.sleep(0.1)
                os.system('clear')
                print("Ctrt+c : Sair do Teste")
                
                a = joystick['lx']
                b = ((a*(-1))+1)/2*1
                print("Direcao",b)
                servo = int((120*b)+(250))
                dev.set_pwm(0,servo)
                print("servo",servo)
                    
                freio = joystick['rx']
                freio = ((freio*(-1))+1)/2*0.5
                print("freio",freio)
                    
                acelerador = joystick['ry']
                acelerador = ((acelerador*(-1))+1)/2*0.5
                print("acelerador",acelerador) 

                sinal_motor = freio+acelerador
                print("sinal_motor",sinal_motor)

                motor = int((220*sinal_motor)+(220))
                
                print("quadrado ",joystick['cross'])
                if (joystick['cross']):
                    dev.set_pwm(1,motor)
                else:
                    dev.set_pwm(1, 330)
                print("motor",motor)

dev.set_pwm(0, 310)
dev.set_pwm(1, 330)
