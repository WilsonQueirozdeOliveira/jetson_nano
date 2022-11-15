from pid_lib import pid

pid = pid(output=0, setpoint=10,feedback=0, Kp=0.1, Ki=10, Kd=0.001)

output = 0 # sensor from output
while True:
    feedback = output # sensor from output
    output = pid.pid_update_(feedback=feedback,setpoint=10)
    print('return output:',output)