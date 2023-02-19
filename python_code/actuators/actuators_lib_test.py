from actuators_lib import Actuators
import time

actuators = Actuators(0, 1)  # Initialize with steering_channel=0, motor_channel=1
actuators.set_steer(50)
time.sleep(1)
actuators.set_motor_forward(10)
time.sleep(1)
actuators.set_motor_forward(0)

