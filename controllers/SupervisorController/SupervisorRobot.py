from controller import Supervisor, Receiver, Emitter

class SupervisorRobot(Supervisor):
    def __init__(self, config, scenario):
        super().__init__()

        self.receiver = self.getDevice('receiver')
        self.emitter = self.getDevice('emitter')
        self.children = self.getRoot().getField('children')

        self.receiver.setChannel(3)
        self.receiver.enable(int(self.getBasicTimeStep()))
        self.emitter.setChannel(3)
        self.activeRobots = {}

        self.config = config
        self.scenario = scenario
        self.phase = -1
        self.init_phase = 1
        self.robotIDs = []

        if config['Scenarios'][scenario]['learningPhase'] == True:
            self.phase = 0
        elif config['Scenarios'][scenario]['goalChoicePhase'] == True:
            self.phase = 1
        else:
            self.phase = 2

        for robotID in config['Scenarios'][scenario]['objects']:
            self.robotIDs += [robotID]


    from memberFunctions import loadRobot
    from memberFunctions import deleteRobot
    from memberFunctions import chooseActionEpisode
    from memberFunctions import update