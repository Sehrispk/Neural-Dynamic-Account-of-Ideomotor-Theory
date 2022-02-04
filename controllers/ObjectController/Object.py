from controller import Robot, Display, Receiver, Emitter, Speaker
import time

class Timer():
    # timer object
    def __init__(self):
        self.run = 0
        self.referenceTime = time.time()
        self.reading = 0

    def start(self):
        self.run = 1
        self.referenceTime = time.time()

    def stop(self):
        self.run = 0

    def reset(self):
        self.referenceTime = time.time()
        self.reading = 0
    
    def update(self):
        if self.run:
            self.reading = time.time() - self.referenceTime

class Object(Robot):
    def __init__(self, color, contingencies, rewardDelay=0, rewardRate=1):
        self.color = color
        self.sound = ""
        self.contingencies = contingencies
        self.rewardDelay = rewardDelay
        self.rewardRate = rewardRate
        
        super().__init__()
        
        self.display = self.getDevice('display')
        self.receiver = self.getDevice('receiver')
        self.emitter = self.getDevice('emitter')
        self.speaker = self.getDevice('speaker')
        self.timer = Timer()
        
        self.receiver.setChannel(2)
        self.receiver.enable(int(self.getBasicTimeStep()))
        self.emitter.setChannel(1)
        
        
    from set_color import set_color
    
    from update import update