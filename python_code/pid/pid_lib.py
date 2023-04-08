import time

class pid:
    def __init__(self, output, setpoint, feedback, Kp, Ki, Kd):
        self.output = output
        self.setpoint = setpoint
        self.feedback = feedback
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.last_time = time.time()
        self.last_erro = 0.0

    def pid_update_(self,feedback,setpoint,delta_time_delay=0.01):
        
        if delta_time_delay:
            time.sleep(delta_time_delay)

        self.feedback = feedback # new feedback
        self.setpoint = setpoint # new setpoint

        delta_time = time.time() - self.last_time 
        self.last_time = time.time()
        print('__________delta_time: ',delta_time)

        erro = self.setpoint - self.feedback
        print('__________erro: ', erro)
        # KP
        KP = erro*self.Kp
        # KI
        KI = erro*(self.Ki*delta_time)
        # KD
        KD = self.Kd*((self.last_erro-erro)/delta_time)
        # camp KD to 0
        if (KD > 1000) or (KD < -1000) :
            KD = 0
        self.last_erro = erro
        #print('KD: ',KD)
        
        # output
        self.output = (feedback + KP + KI + KD)
        #print(self.output)

        return self.output