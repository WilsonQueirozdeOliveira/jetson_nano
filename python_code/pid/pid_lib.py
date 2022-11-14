from time import sleep

class pid:
    def __init__(self, output, setpoint,
        feedback, Kp, Ki, Kd, sample_time):
        self.output = output
        self.setpoint = setpoint
        self.feedback = feedback
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.sample_time = sample_time
        self.last_erro = 0

    def pid_update_(self,feedback,setpoint,sample_time):

        self.feedback = feedback # new feedback
        self.setpoint = setpoint # new setpoint
        self.sample_time = sample_time #new semple_time

        sleep(self.sample_time)

        erro = self.setpoint - self.feedback
        # KP
        KP = erro*self.Kp
        # KI
        KI = erro*(self.Ki*self.sample_time)
        # KD
        KD = self.Kd*((self.last_erro-erro)/self.sample_time)
        # camp KD to 0
        if (KD > 1000) or (KD < -1000) :
            KD = 0
        self.last_erro = erro
        #print('KD: ',KD)
        
        # output
        self.output = (feedback + KP + KI + KD)
        #print(self.output)

        return self.output