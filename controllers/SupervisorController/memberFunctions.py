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


def updateState(self):
    sound = np.zeros(10)
    goal = np.zeros(3)
    action = np.zeros(3)
    target = ''
    
    # read receiver
    while self.receiver.getQueueLength() > 0:
        message = int(str(list(self.receiver.getData())[0]))
        self.receiver.nextPacket()
        if (message >= 500 and message <= 1500):
            sound[message/150-1] = 1
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
                distance = (epuckPosition[0]-objectPosition[0])**2+(epuckPosition[1]-objectPosition[1])**2
                if distance < objDistance:
                    objID = ID
                    objDistance = distance
        target = obj
        
    # update robot states
    self.currentState.objects = {}
    for ID in self.activeRobots:
        if ID == 'e-puck':
            self.currentState.epuck['position'] = self.activeRobots[ID].getPosition()
            self.currentState.epuck['orientation'] = self.activeRobots[ID].getOrientation()
            self.currentState.epuck['goal'] = goal
            self.currentState.epuck['action'] = action
            self.currentState.epuck['actionTarget'] = target
        else:
            self.currentState.objects[ID]['position'] = self.activeRobots[ID].getPosition()
            if target == ID:
                self.currentState.objects[ID]['sound'] = sound
            else:
                self.currentState.objects[ID]['sound'] = 0
            
    # update phase state
    self.updatePhase[str(self.currentState.phase['phase'])](self)

def managePhases(self):
    if self.phase == 0:
        self.emitter.send(bytes(str(self.phase), 'utf-8'))
        if self.init_phase == 1:
            for robotID in self.robotIDs:
                translation = [round(random.uniform(-1, 1), 4), 0.01, round(random.uniform(-1, 1), 4)]
                self.loadRobot(kind='button', ID=robotID, translation=translation)
            self.init_phase = 0
        else:
            if self.action_counter.all(axis=None):
                print('learning phase done')
                for ID in self.robotIDs:
                    self.deleteRobot(ID)
                    self.phase = 1

    elif self.phase == 1:
        # give goal choice command
        print(self.goal)
        self.emitter.send(bytes(str(self.phase), 'utf-8'))
        if any(self.goal) != 0:
            print('goal selection phase done') 
            self.phase = 2

    elif self.phase == 2:
        self.emitter.send(bytes(str(self.phase), 'utf-8'))

        targetRate = int(self.config['Scenarios'][self.scenario]['targetRate'])
        distractorRate = int(self.config['Scenarios'][self.scenario]['distractorRate'])
        queRate = int(self.config['Scenarios'][self.scenario]['queRate'])
        episodeDecision = round(random.uniform(0, 1), 4)

        distractorObjects = []
        targetObjects = []
        distractorSounds = self.goal
        i=0
        while i < len(self.goal):
            if self.goal[i] > 0.5:
                distractorSounds[i] = 0
                for ID in self.robotIDs:
                    if self.contingencies[ID][str(i)] == 0:
                        distractorObjects += [ID]
                    else:
                        targetObjects += [ID]
            else:
                distractorSounds[i] = 1
            i+=1

        if episodeDecision <= targetRate and not self.action_episode:
            #place target
            translation = self.activeRobots['e-puck'].getPosition()
            translation[0] -= self.activeRobots['e-puck'].getOrientation()[2] * 0.3
            translation[2] -= self.activeRobots['e-puck'].getOrientation()[0] * 0.3
            ID = random.choice(targetObjects)
            self.loadRobot(self.children, kind='button', ID=ID, translation=translation)
            self.action_episode = 1

            #mark beginning of action episode
        elif episodeDecision >= targetRate and episodeDecision <= targetRate + distractorRate and not self.action_episode:
            #place distractor
            translation = self.activeRobots['e-puck'].getPosition()
            translation[0] -= self.activeRobots['e-puck'].getOrientation()[2] * 0.3
            translation[2] -= self.activeRobots['e-puck'].getOrientation()[0] * 0.3
            ID = random.choice(distractorObjects)
            self.loadRobot(kind='button', ID=ID, translation=translation)
            self.action_episode = 1
            print("load {}".format(ID))

            #mark beginning of action episode
        elif episodeDecision >= targetRate + distractorRate and distractorRate <= targetRate + distractorRate + queRate and not self.action_episode:
            #play que sound
            #self.playsound()
            print('supervisor should now play sound')
            self.action_episode = 1

            #how to manage action episodes
            #what to measure and when to measure
            #major cleanup of code...

#def inspectState(self):
#        if obj != '':
#            self.action_counter.at[next(x[0] for x in enumerate(self.action) if x[1] > 0.7), obj] += 1

        