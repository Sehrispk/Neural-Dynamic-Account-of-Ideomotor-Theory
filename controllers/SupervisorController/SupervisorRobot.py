from controller import Supervisor, Receiver, Emitter
import pandas as pd
import numpy as np
import time

class Timer():
    # timer object
    def __init__(self, timestep):
        self.timeStep = timestep
        self.simulationTime = 0
        self.run = 0
        self.referenceTime = self.simulationTime
        self.reading = 0

    def start(self):
        self.run = 1
        self.referenceTime = self.simulationTime

    def stop(self):
        self.run = 0

    def reset(self):
        self.referenceTime = self.simulationTime
        self.reading = 0

    def update(self):
        self.simulationTime += self.timeStep
        if self.run:
            self.reading = self.simulationTime - self.referenceTime

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
        self.robotIDs = []
        self.contingencies = {}
        self.phaseList = self.config['Scenarios'][self.scenario]['settings']['phaseList']
        self.phaseIdx = 0
        self.phaseEpisode = 0
            
        for robotID in config['Scenarios'][scenario]['objects']:
            self.robotIDs += [robotID]
            
        for ID in self.robotIDs:
            self.contingencies[ID] = self.config['Scenarios'][self.scenario]['objects'][ID]['contingencies']    
            
        # devices
        self.receiver = self.getDevice('receiver')
        self.emitter = self.getDevice('emitter')
        self.speaker = self.getDevice('speaker')
        self.children = self.getRoot().getField('children')
        self.clock = Timer(self.getBasicTimeStep()/1000)
        self.episodeTimer = Timer(self.getBasicTimeStep()/1000)
        self.distractorTimer = Timer(self.getBasicTimeStep()/1000)
        self.targetTimer = Timer(self.getBasicTimeStep()/1000)
        self.soundTimer = Timer(self.getBasicTimeStep()/1000)
        self.waitTimer = Timer(self.getBasicTimeStep()/1000)

        self.receiver.setChannel(-1)
        self.receiver.enable(int(self.getBasicTimeStep()))
        self.emitter.setChannel(1)
        self.sound = 0
        self.clock.reset()
        self.clock.start()
        
        # active Robots
        self.activeRobots = {}

        # currentState
        self.currentState = WorldState()
        self.currentState.phase['phase'] = self.phaseList[self.phaseIdx]
        self.currentState.phase['actionCounter'] = pd.DataFrame(np.zeros(shape=(3,len(self.robotIDs))), columns=self.robotIDs)
        self.currentState.phase['actionEpisode'] = 0

    from memberFunctions import loadRobot
    from memberFunctions import deleteRobot
    from memberFunctions import startActionEpisode
    from memberFunctions import updatePhase
    from memberFunctions import updateState