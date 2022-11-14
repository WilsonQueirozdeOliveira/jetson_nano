from pid_lib import pid

pid = pid(output=0, setpoint=10,feedback=0, Kp=0.001,
        Ki=100, Kd=1, sample_time=0.01)

output = 0 # sensor from output

while True:
    feedback = output # sensor from output
    output = pid.pid_setpoint_(feedback=feedback,setpoint=10,sample_time=0.01)
    print('return output:',output)