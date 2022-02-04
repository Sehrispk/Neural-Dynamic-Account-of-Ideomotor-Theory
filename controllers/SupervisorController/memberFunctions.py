import copy, random, struct
import numpy as np
from settings import *

def randomPositions(robotIDs):
    translations = {}
    search = 1
    while search:
        for ID in robotIDs:
            translations[ID] = [random.uniform(-arenaSize, arenaSize), 0.01, random.uniform(-arenaSize, arenaSize)]
        search = 0
    
        for ID1 in robotIDs:
            for ID2 in robotIDs:
                distance = ((translations[ID1][0] - translations[ID2][0])**2 + (translations[ID1][2] - translations[ID2][2])**2)
                if distance < objectMinimumDistance and not distance == 0:
                    search = 1

    return translations

def loadRobot(self, kind, ID, translation=[0, 0.01, 0]):
    # creates robotString from config setting and creates robot
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

    transField = self.activeRobots['e-puck'].getField("translation")
    #orienField = self.activeRobots['e-puck'].getField("orientation")
    transField.setSFVec3f([0, 0.0, 0])

    if self.currentState.phase['phase'] == 0:
        print('init phase 0')
        self.startActionEpisode()
    elif self.currentState.phase['phase'] == 1:
        print('init phase 1')
    elif self.currentState.phase['phase'] == 2:
        print('init phase 2')
        self.startActionEpisode()
    return

def startActionEpisode(self):
    self.episodeTimer.stop()
    self.episodeTimer.reset()
    self.distractorTimer.stop()
    self.distractorTimer.reset()
    self.targetTimer.stop()
    self.targetTimer.reset()
    self.soundTimer.stop()
    self.soundTimer.reset()
    
    if self.currentState.phase['phase'] == 0:
        IDs = []
        for ID in self.activeRobots:
            IDs += [ID]
        for ID in IDs:
            if ID != "e-puck":
                self.deleteRobot(ID)

        translations = randomPositions(self.robotIDs)
        for ID, translation in translations.items():
            self.loadRobot(kind='button', ID=ID, translation=translation)
    elif self.currentState.phase['phase'] == 1:
        transField = self.activeRobots['e-puck'].getField("translation")
        #orienField = self.activeRobots['e-puck'].getField("orientation")
            
        INITIAL = [0, 0.0, 0]
        transField.setSFVec3f(INITIAL)
        return
    elif self.currentState.phase['phase'] == 2:
        transField = self.activeRobots['e-puck'].getField("translation")
        #orienField = self.activeRobots['e-puck'].getField("orientation")
        transField.setSFVec3f([0, 0, 0])
    
        IDs = []
        for ID in self.activeRobots:
            IDs += [ID]
        for ID in IDs:
            if ID != "e-puck":
                self.deleteRobot(ID)
        
        targetRate = self.config['Scenarios'][self.scenario]['settings']['targetRate']
        distractorRate = self.config['Scenarios'][self.scenario]['settings']['distractorRate']
        queRate = self.config['Scenarios'][self.scenario]['settings']['queRate']
        episodeDecision = random.uniform(0, 1)

        distractorObjects = []
        targetObjects = []
        distractorSounds = np.zeros(len(self.currentState.epuck['goal']))
        i = 0
        while i < len(self.currentState.epuck['goal']):
            if self.currentState.epuck['goal'][i] > stateThreshold:
                distractorSounds[i] = 0
                for ID in self.robotIDs:
                    if self.contingencies[ID][str(i)] == 0:
                        distractorObjects += [ID]
                    else:
                        targetObjects += [ID]
            else:
                distractorSounds[i] = 1
            i += 1

        # chose random objects/sounds if no goal is selected
        if len(targetObjects) == 0:
            targetObjects += [random.choice(self.robotIDs)]
        if len(distractorObjects) == 0:
            distractorObjects += [random.choice(self.robotIDs)]
        if not any(distractorSounds > stateThreshold):
            r = random.choice([0, 1, 2])
            distractorSounds[r] = 1

        if episodeDecision <= targetRate:
            #place target
            translation = transField.getSFVec3f()
            translation[0] -= self.activeRobots['e-puck'].getOrientation()[2] * objectPlaceDistance + random.uniform(-objectPlaceNoise, objectPlaceNoise)
            translation[1] = 0.01
            translation[2] -= self.activeRobots['e-puck'].getOrientation()[0] * objectPlaceDistance + random.uniform(-objectPlaceNoise, objectPlaceNoise)
            try:
                ID = random.choice(targetObjects)
                self.loadRobot(kind='button', ID=ID, translation=translation)
                print("supervisor places target object")
            except:
                print("no target object")
            self.targetTimer.start()

        elif episodeDecision >= targetRate and episodeDecision <= targetRate + distractorRate:
            #place distractor
            translation = transField.getSFVec3f()
            translation[0] -= self.activeRobots['e-puck'].getOrientation()[2] * objectPlaceDistance + random.uniform(-objectPlaceNoise, objectPlaceNoise)
            translation[1] = 0.01
            translation[2] -= self.activeRobots['e-puck'].getOrientation()[0] * objectPlaceDistance + random.uniform(-objectPlaceNoise, objectPlaceNoise)
            try:
                ID = random.choice(distractorObjects)
                self.loadRobot(kind='button', ID=ID, translation=translation)
                print("supervisor places distractor object")
            except:
                print("no distractor object")
            self.distractorTimer.start()

        elif episodeDecision >= targetRate + distractorRate and distractorRate <= targetRate + distractorRate + queRate:
            #play que sound
            idx = random.choice([i for i,val in enumerate(distractorSounds) if val==1])
            if not self.speaker.isSoundPlaying(""):
                self.sound = frequencies[idx]
                self.speaker.playSound(self.speaker, self.speaker, soundPath+str(frequencies[idx])+"Hz.wav", 1, 1, 0, False)
                        
            print('supervisor plays sound {}Hz'.format(self.sound))
            self.soundTimer.start()
    self.updateState()

def updatePhase(self):
    # log actions
    if all(x < 0.5 for x in self.currentState.epuck['action'][:,0]) and any(self.currentState.epuck['action'][:,1]) > 0.5:
        self.currentState.phase['actionEpisode'] += 1
        idx = [i for i,val in enumerate(self.currentState.epuck['action'][:,1]) if val==1][0]
        print("actionEpisode: {}".format(self.currentState.phase['actionEpisode']))
        print("action {} on {}".format(idx, self.currentState.epuck['actionTarget']))
        self.currentState.phase['actionCounter'][self.currentState.epuck['actionTarget'][1]][idx] += 1
        print(self.currentState.phase['actionCounter'])
        self.episodeTimer.start()

    # phase completion conditions
    if self.currentState.phase['phase'] == 0 and self.currentState.phase['actionCounter'].all(axis=None) > 0 and self.episodeTimer.reading > episodeTimeout:
        print("learning phase done")
        self.currentState.phase['phase'] += 1
        self.initPhase()
    elif self.currentState.phase['phase'] == 1 and any(self.currentState.epuck['goal']) > stateThreshold:
        print("goal selection phase done")
        self.currentState.phase['phase'] += 1
        self.initPhase()
    elif self.currentState.phase['phase'] == 1 and self.currentState.phase['actionEpisode'] >= N_goalReach:
        print("goal performance phase done")
        self.currentState.phase['phase'] = 1
        self.initPhase()

    # start new action episode
    if self.episodeTimer.reading > episodeTimeout or self.distractorTimer.reading > distractorTimeout or self.soundTimer.reading > soundTimeout or self.targetTimer.reading > targetTimeout:
        self.startActionEpisode()

def updateState(self):
    # send task information to epuck
    self.emitter.send(bytes(str(self.currentState.phase['phase']), 'utf-8'))
    if self.speaker.isSoundPlaying(""):
        packet = np.zeros(10)
        packet[round(self.sound/150-1)] = 1
        message = struct.pack('%sf' % len(packet), *packet)
        self.emitter.send(message)

    # read receiver
    sound = np.zeros(10)
    goal = np.zeros(3)
    led = np.zeros(9)
    action = np.zeros(3)
    target = ''
    while self.receiver.getQueueLength() > 0:
        packet = struct.unpack('%sf' % int((self.receiver.getData().__sizeof__()-33)/4), self.receiver.getData())
        #message = int(str(list(self.receiver.getData())[0]))
        if (len(packet) == 10):
            sound = list(packet)
        elif (len(packet) == 9):
            led = list(packet)
        elif (len(packet) == 3):
            goal = list(packet)
        self.receiver.nextPacket()

    # determine action status
    i = 0
    while i < len(led)/3:
        if led[3*i] >= 0.5 and led[3*i+1] >= 0.5 and led[3*i+2] >= 0.5:
            action[i] = 1
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
        i += 1
    
    """if not all(a == 0 for a in action):
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
        target = objID"""
        
    # update robot status
    self.currentState.objects = {}
    for ID in self.activeRobots:
        if ID == 'e-puck':
            self.currentState.epuck['position'] = self.activeRobots[ID].getPosition()
            self.currentState.epuck['orientation'] = self.activeRobots[ID].getOrientation()
            self.currentState.epuck['led'] = led
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
                self.currentState.objects[ID]['sound'] = np.zeros(10)
            
    # update timer
    self.episodeTimer.update()
    self.distractorTimer.update()
    self.targetTimer.update()
    self.soundTimer.update()
    self.clock.update()
    
    # reset epuck if out of bounds
    if abs(self.activeRobots['e-puck'].getPosition()[0]) > resetBound or abs(self.activeRobots['e-puck'].getPosition()[2]) > resetBound:
        transField = self.activeRobots['e-puck'].getField("translation")
        #orienField = self.activeRobots['e-puck'].getField("orientation")
        transField.setSFVec3f([0, 0.0, 0])
