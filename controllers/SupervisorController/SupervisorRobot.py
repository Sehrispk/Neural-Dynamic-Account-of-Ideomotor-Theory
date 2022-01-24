from controller import Supervisor, Receiver, Emitter
import pandas as pd
import numpy as np

class SupervisorRobot(Supervisor):
    def __init__(self, config, scenario):
        super().__init__()

        self.receiver = self.getDevice('receiver')
        self.emitter = self.getDevice('emitter')
        self.children = self.getRoot().getField('children')

        self.receiver.setChannel(-1)
        self.receiver.enable(int(self.getBasicTimeStep()))
        self.emitter.setChannel(1)
        self.activeRobots = {}

        self.config = config
        self.scenario = scenario
        self.phase = 0
        self.init_phase = 1
        self.robotIDs = []
        self.contingencies = {}

        if config['Scenarios'][scenario]['learningPhase'] == True:
            self.phase = 0
        elif config['Scenarios'][scenario]['goalChoicePhase'] == True:
            self.phase = 1
        else:
            self.phase = 2

        for robotID in config['Scenarios'][scenario]['objects']:
            self.robotIDs += [robotID]

        for ID in self.robotIDs:
            self.contingecies[ID] = self.config['Scenarios'][self.scenario]['distractorRate']['objects'][ID]['contingencies']

        # defines the state of the scenario
        self.sound = np.zeros(10)
        self.action = np.zeors(3)
        self.goal = np.zeros(3)
        self.targetObject = ''
        self.action_episode = 0
        self.action_counter = pd.DataFrame(np.zeros(shape=(3,len(self.robotIDs))), columns=self.robotIDs)


    from memberFunctions import loadRobot
    from memberFunctions import deleteRobot
    from memberFunctions import chooseActionEpisode
    from memberFunctions import managePhases
    from memberFunctions import inspectState