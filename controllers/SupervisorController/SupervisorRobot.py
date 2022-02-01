from controller import Supervisor, Receiver, Emitter
import pandas as pd
import numpy as np
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

class WorldState():
    # wrapper class for relevant world variables
    epuck = {} # {'position': [0, 0, 0.2], 'orientation': np.zeros(2), 'goal': np.zeros(3), 'action': np.zeros(3,2), 'actionTarget': ['', '']}
    objects = {} # {'ID': {'color': '', 'position': [0,0,0], 'sound': ''}, ...}
    phase = {} # {'phase': 0, 'actionEpisode': 0, 'actionCounter': pd.DataFrame(np.zeros(shape=(3,len(self.robotIDs))), columns=self.robotIDs)}

class SupervisorRobot(Supervisor):
    def __init__(self, config, scenario):
        super().__init__()

        # settings
        self.config = config
        self.scenario = scenario
        # scenario settings
        initialPhase = -1
        self.robotIDs = []
        self.contingencies = {}
        if config['Scenarios'][scenario]['settings']['learningPhase'] == True:
            initialPhase = 0
        elif config['Scenarios'][scenario]['settings']['goalChoicePhase'] == True:
            initialPhase = 1
        else:
            initialPhase = 2
            
        for robotID in config['Scenarios'][scenario]['objects']:
            self.robotIDs += [robotID]
            
        for ID in self.robotIDs:
            self.contingencies[ID] = self.config['Scenarios'][self.scenario]['objects'][ID]['contingencies']    
            
        # devices
        self.receiver = self.getDevice('receiver')
        self.emitter = self.getDevice('emitter')
        self.speaker = self.getDevice('speaker')
        self.children = self.getRoot().getField('children')
        self.episodeTimer = Timer()
        self.distractorTimer = Timer()
        self.targetTimer = Timer()
        self.soundTimer = Timer()

        self.receiver.setChannel(-1)
        self.receiver.enable(int(self.getBasicTimeStep()))
        self.emitter.setChannel(1)
        self.sound = 0
        
        # active Robots
        self.activeRobots = {}

        # currentState
        self.currentState = WorldState()
        self.currentState.phase['phase'] = initialPhase
        self.currentState.phase['actionCounter'] = pd.DataFrame(np.zeros(shape=(3,len(self.robotIDs))), columns=self.robotIDs)
        self.currentState.phase['actionEpisode'] = 0


    from memberFunctions import loadRobot
    from memberFunctions import deleteRobot
    from memberFunctions import initPhase
    from memberFunctions import startActionEpisode
    from memberFunctions import updatePhase
    from memberFunctions import updateState