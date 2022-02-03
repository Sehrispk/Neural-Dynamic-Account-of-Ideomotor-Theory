from math import sqrt
import numpy as np
import struct, random
def update(self):
    if self.receiver.getQueueLength():
        distance = 1/sqrt(self.receiver.getSignalStrength())
        #action = str(list(self.receiver.getData())[0])

        packet = struct.unpack('%sf' % self.receiver.getDataSize()/sys.getsizeof(float), receiver.getData())
        
        #if distance < 0.23 and (int(action) >= 0 and int(action) <= 2):
        #    if self.contingencies[action] != 0:
        #        self.sound = self.contingencies[action]
        #        if not self.timer.run:
        #            self.timer.start()
        #self.receiver.nextPacket()

        if len(distance) < 0.23 and packet == 9:
            i = 0
            while i < len(packet)/3:
                i += 1
                if packet[3*i] >= 0.5 and packet[3*i+1] >= 0.5 and packer[3*i+2] >= 0.5 and self.contingencies[str(i)] != 0:
                    self.sound = self.contingencies[str(i)]
                    if not self.timer.run:
                        self.timer.start()
        self.receiver.nextPacket()


    if self.timer.reading > self.rewardDelay and not self.speaker.isSoundPlaying(""):
        rewardDecision = random.uniform(0, 1)
        if rewardDecision <= self.rewardRate:
            self.speaker.playSound(self.speaker, self.speaker, str(self.sound)+"Hz.wav", 1, 1, 0, False)
        self.timer.stop()
        self.timer.reset()

    if self.speaker.isSoundPlaying(""):
        packet = np.zeros(10)
        packet[round(self.sound/150-1)] = 1
        message = struct.pack('%sf' % len(packet), *packet)
        self.emitter.send(message)

    self.timer.update()