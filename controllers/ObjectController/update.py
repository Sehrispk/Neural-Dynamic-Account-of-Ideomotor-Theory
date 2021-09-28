from math import sqrt
import struct
def update(self):
    if self.receiver.getQueueLength():
        distance = 1/sqrt(self.receiver.getSignalStrength())
        
        if distance < 0.2:
            action = str(list(self.receiver.getData())[0])
            if self.contingencies[action] != "0":
                self.speaker.playSound(self.speaker, self.speaker, self.contingencies[action]+"Hz.wav", 1, 1, 0, False)
        self.receiver.nextPacket()