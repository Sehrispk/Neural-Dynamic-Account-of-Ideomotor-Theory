from controller import Supervisor, Receiver, Emitter
import pandas as pd
import numpy as np

class phaseFunctionWrapper():
    def __init__(self):
        return

    def updatePhase0(self):
        print('that worked0')
    
    def updatePhase1(self):
        print('that worked1')
    
    def updatePhase2(self):
        print('that worked2')

class WorldState():
    # wrapper class for relevant world variables
    epuck = {} # {'position': [0, 0, 0.2], 'orientation': np.zeros(2), 'goal': np.zeros(3), 'action': np.zeros(3), 'actionTarget': ''}
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
        self.children = self.getRoot().getField('children')

        self.receiver.setChannel(-1)
        self.receiver.enable(int(self.getBasicTimeStep()))
        self.emitter.setChannel(1)
        
        # active Robots
        self.activeRobots = {}

        # currentState
        self.currentState = WorldState()
        self.currentState.phase['phase'] = initialPhase
        
        self.updatePhase = {'0':phaseFunctionWrapper.updatePhase0, '1': phaseFunctionWrapper.updatePhase1, '2':phaseFunctionWrapper.updatePhase2}


    from memberFunctions import loadRobot
    from memberFunctions import deleteRobot
    from memberFunctions import updateState
    from memberFunctions import managePhases