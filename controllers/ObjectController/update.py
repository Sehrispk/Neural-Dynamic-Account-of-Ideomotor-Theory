from math import sqrt
import struct
def update(self):
    if self.receiver.getQueueLength():
        distance = 1/sqrt(self.receiver.getSignalStrength())
        action = str(list(self.receiver.getData())[0])
        
        if distance < 0.23 and (int(action) >= 0 and int(action) <= 2):
            if self.contingencies[action] != 0:
                self.sound = self.contingencies[action]
                if not self.speaker.isSoundPlaying(""):
                    self.speaker.playSound(self.speaker, self.speaker, str(self.sound)+"Hz.wav", 1, 1, 0, False)
        self.receiver.nextPacket()

    if self.speaker.isSoundPlaying(""):
        self.emitter.send(bytes(str(self.sound), 'utf-8'))