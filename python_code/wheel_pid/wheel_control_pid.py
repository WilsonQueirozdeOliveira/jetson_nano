import sys
sys.path.insert(1, '../pid')
sys.path.insert(1, '../sensors')
from pid_lib import pid
from sensors_lib import wheel_sensor
from pca9685_driver import Device

dev = Device(0x40,1)
dev.set_pwm_frequency(50)

wheel_output_pwm = 1

whell_rear_left = wheel_sensor(gpio_input=15,tire_diameter_m=0.067)

pid_whell = pid(output=0, setpoint=3,feedback=0, Kp=0.1, Ki=1, Kd=0)

pid_wheel_output_pwm = 300

dev.set_pwm(wheel_output_pwm, pid_wheel_output_pwm)

count = 0
while count < 200:
    count += 1
    print('count: ', count)
    print('m/s: ', whell_rear_left.speed_meters_per_second())

    feedback = whell_rear_left.speed_meters_per_second() # sensor from output
    pid_output = pid_whell.pid_update_(feedback=feedback,setpoint=3)
    print('pid_output:',pid_output)

    pid_wheel_output_pwm = int(330-(pid_output)+0.2)

    print('pid_wheel_output_pwm: ',pid_wheel_output_pwm)

    if pid_wheel_output_pwm > 330:
        pid_wheel_output_pwm = 330

    if pid_wheel_output_pwm < 300:
        pid_wheel_output_pwm = 300

    dev.set_pwm(wheel_output_pwm, pid_wheel_output_pwm)

    #safety

    #pid_wheel_output_pwm = 330

    dev.set_pwm(wheel_output_pwm, pid_wheel_output_pwm)

pid_wheel_output_pwm = 330

dev.set_pwm(wheel_output_pwm, pid_wheel_output_pwm)