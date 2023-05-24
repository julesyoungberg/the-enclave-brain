from control import send_osc

class OSCTransition:
    def __init__(self, address: str, start: float, end: float, duration: float):
        self.address = address
        self.start = start
        self.end = end
        self.time = 0.0
        self.duration = duration
        self.done = False
    
    def step(self, dt: float):
        send_osc(self.address, (self.time / self.duration) * (self.end - self.start) + self.start)
        self.time += dt
        if self.time > self.duration:
            self.done = True    
