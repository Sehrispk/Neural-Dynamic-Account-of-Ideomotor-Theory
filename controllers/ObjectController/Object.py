from controller import Robot
from controller import Display
from controller import Receiver
from controller import Emitter

class Object(Robot):
    def __init__(self, contingencies):
        self.color = [0, 0, 0]
        self.sound = ""
        self.contingencies = contingencies
        
        super().__init__()
        
        self.display = self.getDevice('display')
        self.receiver = self.getDevice('receiver')
        self.emitter = self.getDevice('emitter')
        self.speaker = self.getDevice('speaker')
        
        self.receiver.setChannel(1)
        self.receiver.enable(int(self.getBasicTimeStep()))
        self.emitter.setChannel(2)
        
        
    from set_color import set_color
    
    from update import update