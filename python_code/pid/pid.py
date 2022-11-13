from time import sleep

setpoint = 10

output = 0

feedback = 0

Kp=0.001

Ki=10

Kd=1

sample_time = .2

last_erro = 0

def pid(setpoint, feedback, output):
    sleep(sample_time)

    erro = setpoint - feedback

    KP = erro*Kp

    KI = erro*Ki*sample_time

    last_erro = erro

    KD = Kd*((last_erro-erro)/sample_time)

    output = (output + KP + KI + KD)

    return output

while True:
    output = pid(setpoint, feedback, output)
    print('output=', output)
    feedback = output # sensor from output

