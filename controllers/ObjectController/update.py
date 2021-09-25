
def update(self):
    if self.receiver.getQueueLength():
        distance = 1/sqrt(self.receiver.getSignalStrength())
        
        if distance < 0.2:
            data = self.receiver.getData()
            #if self.dependencies["Action "+data] not "None":
            #    self.speaker.playSound(self.speaker, self.speaker, "TestSound.wav", 1, 1, 0, 0)