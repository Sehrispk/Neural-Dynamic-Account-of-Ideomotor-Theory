from math import sqrt
import struct
def update(self):
    self.sound = "-1"
    if self.receiver.getQueueLength():
        distance = 1/sqrt(self.receiver.getSignalStrength())
        action = str(list(self.receiver.getData())[0])
        
        if distance < 0.23 and action != "254":
            if self.contingencies[action] != "0":
                self.sound = self.contingencies[action]
                if not self.speaker.isSoundPlaying(""):
                    self.speaker.playSound(self.speaker, self.speaker, self.sound+"Hz.wav", 1, 1, 0, False)
        self.receiver.nextPacket()
        
    self.emitter.send(bytes(self.sound, 'utf-8'))