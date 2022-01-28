import copy, random
import numpy as np

def loadRobot(self, kind, ID, translation=[0, 0.01, 0]):
    # creates robotString from config setting, creates robot and returns robot node
    robot_conf = copy.deepcopy(self.config['Robots'][kind])
    try:
        robot_conf['controllerArgs'] = self.config['Scenarios'][self.scenario]['objects'][ID]
        robot_conf['name'] = "\"{}\"".format(ID)

        translation_string = str(translation[0]) + " " + str(translation[1]) + " " + str(translation[2])
        robot_conf['translation'] = translation_string
        print('load {}'.format(ID))
    except:
        print('load default {}'.format(ID))

    controllerArgs = '['
    args = ''
    for key,value in robot_conf['controllerArgs'].items():
        controllerArgs += '\"{}\", '.format(value)
    controllerArgs += ']'
    for key,value in robot_conf.items():
        if key != 'controllerArgs' and key != 'type':
            args += key + ' ' + value + ', '
    args += 'controllerArgs ' + str(controllerArgs)
    robotString = '{0} {{{1}}}'.format(robot_conf['type'], args)
    self.children.importMFNodeFromString(-1, robotString)
    self.activeRobots[ID] = self.children.getMFNode(-1)

def deleteRobot(self, ID):
    if ID in self.activeRobots:
        robot = self.activeRobots.pop(ID)
        robot.remove()

def initPhase(self):
    IDs = []
    for ID in self.activeRobots:
        IDs += [ID]
    for ID in IDs:
        if ID != "e-puck":
            self.deleteRobot(ID)

    if self.currentState.phase['phase'] == 0:
        print('init phase 0')
        for robotID in self.robotIDs:
            translation = [round(random.uniform(-1, 1), 4), 0.01, round(random.uniform(-1, 1), 4)]
            self.loadRobot(kind='button', ID=robotID, translation=translation)
        return
    elif self.currentState.phase['phase'] == 1:
        print('init phase 1')
        return
    elif self.currentState.phase['phase'] == 2:
        print('init phase 2')
        self.startActionEpisode()
        return

def startActionEpisode(self):
    if self.currentState.phase['phase'] == 0:
        return
    elif self.currentState.phase['phase'] == 1:
        return
    elif self.currentState.phase['phase'] == 2:
        IDs = []
        for ID in self.activeRobots:
            IDs += [ID]
        for ID in IDs:
            if ID != "e-puck":
                self.deleteRobot(ID)
        targetRate = int(self.config['Scenarios'][self.scenario]['settings']['targetRate'])
        distractorRate = int(self.config['Scenarios'][self.scenario]['settings']['distractorRate'])
        queRate = int(self.config['Scenarios'][self.scenario]['settings']['queRate'])
        episodeDecision = round(random.uniform(0, 1), 4)

        distractorObjects = []
        targetObjects = []
        distractorSounds = self.currentState.epuck['goal']
        i = 0
        while i < len(self.currentState.epuck['goal']):
            if self.currentState.epuck['goal'][i] > 0.5:
                distractorSounds[i] = 0
                for ID in self.robotIDs:
                    if self.contingencies[ID][str(i)] == 0:
                        distractorObjects += [ID]
                    else:
                        targetObjects += [ID]
            else:
                distractorSounds[i] = 1
            i += 1

        if episodeDecision <= targetRate:
            #place target
            translation = self.activeRobots['e-puck'].getPosition()
            translation[0] -= self.activeRobots['e-puck'].getOrientation()[2] * 0.5
            translation[2] -= self.activeRobots['e-puck'].getOrientation()[0] * 0.5
            ID = random.choice(targetObjects)
            self.loadRobot(kind='button', ID=ID, translation=translation)
            print("load {}".format(ID))

            #mark beginning of action episode
        elif episodeDecision >= targetRate and episodeDecision <= targetRate + distractorRate:
            #place distractor
            translation = self.activeRobots['e-puck'].getPosition()
            translation[0] -= self.activeRobots['e-puck'].getOrientation()[2] * 0.5
            translation[2] -= self.activeRobots['e-puck'].getOrientation()[0] * 0.5
            try:
                ID = random.choice(distractorObjects)
                self.loadRobot(kind='button', ID=ID, translation=translation)
                print("load {}".format(ID))
            except:
                print("no ditractor object")

            #mark beginning of action episode
        elif episodeDecision >= targetRate + distractorRate and distractorRate <= targetRate + distractorRate + queRate:
            #play que sound
            #self.playsound()
            #and place object?
            print('supervisor should now play sound')

def updatePhase(self):
    # log actions
    if all(x < 0.5 for x in self.currentState.epuck['action'][:,0]) and any(self.currentState.epuck['action'][:,1]) > 0.5:
        self.currentState.phase['actionEpisode'] += 1
        idx = [i for i,val in enumerate(self.currentState.epuck['action'][:,1]) if val==1][0]
        print(self.currentState.phase['actionEpisode'])
        print(idx)
        print(self.currentState.epuck['actionTarget'])
        self.currentState.phase['actionCounter'][self.currentState.epuck['actionTarget'][1]][idx] += 1 
        print(self.currentState.phase['actionCounter'])
        self.episodeTimer.start()

    # phase completion conditions
    if self.currentState.phase['phase'] == 0 and self.currentState.phase['actionCounter'].all(axis=None) > 0:
        print("learning phase done")
        self.currentState.phase['phase'] += 1
        self.initPhase()
        self.updateState()
    elif self.currentState.phase['phase'] == 1 and any(self.currentState.epuck['goal']) > 0.5:
        print("goal selection phase done")
        self.currentState.phase['phase'] += 1
        self.initPhase()
        self.updateState()
    elif self.currentState.phase['phase'] == 1 and self.currentState.phase['actionEpisode'] > 10000:
        print("goal performance phase done")
        self.currentState.phase['phase'] = 0
        self.initPhase()
        self.updateState()

    # start new action episode
    if self.episodeTimer.reading > 5:
        self.startActionEpisode()
        self.episodeTimer.stop()
        self.episodeTimer.reset()

def updateState(self):
    # send task information to epuck
    self.emitter.send(bytes(str(self.currentState.phase['phase']), 'utf-8'))

    # read receiver
    sound = 0
    goal = np.zeros(3)
    action = np.zeros(3)
    target = ''
    while self.receiver.getQueueLength() > 0:
        message = int(str(list(self.receiver.getData())[0]))
        self.receiver.nextPacket()
        if (message >= 500 and message <= 1500):
            sound = message
        elif (message >=0 and message <= 2):
            action[message] = 1
        elif (message >= 5 and message <= 15):
            goal[int(message/5-1)] = 1

    # determine action status
    if not all(a == 0 for a in action):
        epuckPosition = self.activeRobots['e-puck'].getPosition()
        objID = ''
        objDistance = 10
        for ID in self.activeRobots:
            if not ID == 'e-puck':
                objectPosition = self.activeRobots[ID].getPosition()
                distance = (epuckPosition[0]-objectPosition[0])**2+(epuckPosition[2]-objectPosition[2])**2
                
                if distance < objDistance:
                    objID = ID
                    objDistance = distance
        target = objID
        
    # update robot status
    self.currentState.objects = {}
    for ID in self.activeRobots:
        if ID == 'e-puck':
            self.currentState.epuck['position'] = self.activeRobots[ID].getPosition()
            self.currentState.epuck['orientation'] = self.activeRobots[ID].getOrientation()
            self.currentState.epuck['goal'] = goal
            self.currentState.epuck['action'][:, 1] = self.currentState.epuck['action'][:, 0]
            self.currentState.epuck['action'][:, 0] = action
            self.currentState.epuck['actionTarget'][1] = self.currentState.epuck['actionTarget'][0]
            self.currentState.epuck['actionTarget'][0] = target
        else:
            self.currentState.objects[ID] = {}
            self.currentState.objects[ID]['position'] = self.activeRobots[ID].getPosition()
            if target == ID:
                self.currentState.objects[ID]['sound'] = sound
            else:
                self.currentState.objects[ID]['sound'] = 0
            
    # update timer
    self.episodeTimer.update()
    self.distractorTimer.update()
