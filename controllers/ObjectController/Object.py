from controller import Robot, Display, Receiver, Emitter, Speaker

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
        
        self.receiver.setChannel(2)
        self.receiver.enable(int(self.getBasicTimeStep()))
        self.emitter.setChannel(1)
        
        
    from set_color import set_color
    
    from update import update