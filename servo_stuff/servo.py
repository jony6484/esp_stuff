import machine

class Servo:
    def __init__(self, pin_num, freq=50, ang0=0, ang1=180, duty0=20, duty1=120):
        self.ang0 = ang0
        self.ang1 = ang1
        self.duty0 = duty0
        self.duty1= duty1
        self.freq = freq
        self.pwm = machine.PWM(machine.Pin(pin_num, machine.Pin.OUT))
        self.pwm.freq(freq)
        self.pwm.duty(0)

    def angle2duty(self, angle):
        return int(self.duty0 + (angle - self.ang0)*(self.duty1 - self.duty0)/(self.ang1 - self.ang0))

    def move(self, angle):
        self.pwm.duty(self.angle2duty(angle))

