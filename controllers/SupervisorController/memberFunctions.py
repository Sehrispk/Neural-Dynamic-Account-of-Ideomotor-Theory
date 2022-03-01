import copy, random, struct
import numpy as np
from settings import *
from util import *

def phasePauseComplete(currentState, phaseEpisode, clock, episodeTimer):
    if clock.reading > Tinit and episodeTimer.reading > 2:
        print("pause complete...")
        return 1
    else:
        if episodeTimer.reading == 0:
            episodeTimer.start()
        return 0
        
def phaseExploreComplete(currentState, phaseEpisode, clock, episodeTimer):
    #if currentState.phase['actionCounter'].all(axis=None) > 0 and episodeTimer.reading > episodeTimeout:
    if clock.reading > 2*Tinit:
        print("learning phase done...")
        return 1
    else:
        return 0
        
def phaseTestComplete(currentState, phaseEpisode, clock, episodeTimer):
    if phaseEpisode > N_goal:
        print("test phase done...")
        return 1
    else:
        return 0
        
def phaseSwitchComplete(currentState, phaseEpisode, clock, episodeTimer):
    if phaseEpisode > 2:
        print("switch phase done...")
        return 1
    else:
        return 0
        
def phaseRepititionComplete(currentState, phaseEpisode, clock, episodeTimer):
    if phaseEpisode > N_repitition:
        print("repitition phase done...")
        return 1
    else:
        return 0
        
def phaseEndComplete(currentState, phaseEpisode, clock, episodeTimer):
    if episodeTimer.reading > 2:
        return 1
    else:
        return 0
        
def phasePauseEpisode(self):
    # wait
    self.episodeTimer.start()
    return 0
    
def phaseExploreEpisode(self):
    translations = randomPositions(self.currentState.epuck['position'], self.robotIDs)
    for ID, translation in translations.items():
        self.loadRobot(kind='button', ID=ID, translation=translation)
    return 1
        
def phaseTestEpisode(self):
    # place target and distractor for goal
    if any([g > stateThreshold for g in self.currentState.epuck['goal']]):
        # reset epuck position
        transField = self.activeRobots['e-puck'].getField("translation")
        #orienField = self.activeRobots['e-puck'].getField("orientation")
        transField.setSFVec3f([0, 0, 0])
        
        distractorObjects = []
        targetObjects = []
        for ID in self.robotIDs:
            if self.contingencies[ID][str(self.currentState.phase['phase']-2)] == 0:
                distractorObjects += [ID]
            else:
                targetObjects += [ID]
        
        #place objects
        translation = transField.getSFVec3f()
        translation[0] -= self.activeRobots['e-puck'].getOrientation()[2] * objectPlaceDistance
        translation[1] = 0.01
        translation[2] -= self.activeRobots['e-puck'].getOrientation()[0] * objectPlaceDistance 
        if self.phaseEpisode == 0 or self.phaseEpisode == 2:
            translation[0] += objectMinimumDistance/2 * translation[2]
            translation[2] -= objectMinimumDistance/2 * translation[0]
            ID = random.choice(distractorObjects)
            self.loadRobot(kind='button', ID=ID, translation=translation)
            print("supervisor places distractor object: {}".format(ID))
            self.distractorTimer.start()
        if self.phaseEpisode >= 1:
            translation[0] -= objectMinimumDistance/2 * translation[2]
            translation[2] += objectMinimumDistance/2 * translation[0]
            ID = random.choice(targetObjects)
            self.loadRobot(kind='button', ID=ID, translation=translation)
            print("supervisor places target object: {}".format(ID))
            self.targetTimer.start()
        return 1
    else:
        # wait until goal has formed
        self.episodeTimer.start()
        return 0
    
def phaseSwitchEpisode(self):
    if any([g > stateThreshold for g in self.currentState.epuck['goal']]):
        # reset epuck position
        transField = self.activeRobots['e-puck'].getField("translation")
        #orienField = self.activeRobots['e-puck'].getField("orientation")
        transField.setSFVec3f([0, 0, 0])
        
        # determine distractor and target objects and sounds
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
                
        if self.phaseEpisode == 0:
            translation = transField.getSFVec3f()
            translation[0] -= self.activeRobots['e-puck'].getOrientation()[2] * objectPlaceDistance
            translation[1] = 0.01
            translation[2] -= self.activeRobots['e-puck'].getOrientation()[0] * objectPlaceDistance 
            ID = random.choice(distractorObjects)
            self.loadRobot(kind='button', ID=ID, translation=translation)
            print("supervisor places distractor object: {}".format(ID))
            self.distractorTimer.start()
        else: 
            translation = transField.getSFVec3f()
            translation[0] -= self.activeRobots['e-puck'].getOrientation()[2] * objectPlaceDistance
            translation[1] = 0.01
            translation[2] -= self.activeRobots['e-puck'].getOrientation()[0] * objectPlaceDistance 
            ID = random.choice(targetObjects)
            self.loadRobot(kind='button', ID=ID, translation=translation)
            print("supervisor places target object: {}".format(ID))
            self.targetTimer.start()
        return 1
    else:
        # wait for goal
        self.episodeTimer.start()
        return 0
    
def phaseRepititionEpisode(self):
    # determine distractor and target objects and sounds
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

    # chose random distractor objects/sounds if no goal is selected
    if len(distractorObjects) == 0:
        distractorObjects += [random.choice(self.robotIDs)]
    if not any(distractorSounds > stateThreshold):
        r = random.choice([0, 1, 2])
        distractorSounds[r] = 1

    # reset epuck position
    transField = self.activeRobots['e-puck'].getField("translation")
    #orienField = self.activeRobots['e-puck'].getField("orientation")
    transField.setSFVec3f([0, 0, 0])
    
    # determin next action episode
    if self.config['Scenarios'][self.scenario]['settings']['customSequence']:
        try:
            if self.config['Scenarios'][self.scenario]['settings']['customSequence'][self.phaseEpisode] == 't':
                targetRate = 1
                distractorRate = 0
                queRate = 0
            if self.config['Scenarios'][self.scenario]['settings']['customSequence'][self.phaseEpisode] == 'd':
                targetRate = 0
                distractorRate = 1
                queRate = 0
            if self.config['Scenarios'][self.scenario]['settings']['customSequence'][self.phaseEpisode] == 'q':
                targetRate = 0
                distractorRate = 0
                queRate = 1
        except Exception as e:
            print(e)
            print('invalid sequence string, continue with default rates')
            targetRate = self.config['Scenarios'][self.scenario]['settings']['targetRate']
            distractorRate = self.config['Scenarios'][self.scenario]['settings']['distractorRate']
            queRate = self.config['Scenarios'][self.scenario]['settings']['queRate']
    else: 
        targetRate = self.config['Scenarios'][self.scenario]['settings']['targetRate']
        distractorRate = self.config['Scenarios'][self.scenario]['settings']['distractorRate']
        queRate = self.config['Scenarios'][self.scenario]['settings']['queRate']
        
    episodeDecision = random.uniform(0, 1)
    if episodeDecision <= targetRate:
        #place target
        translation = transField.getSFVec3f()
        translation[0] -= self.activeRobots['e-puck'].getOrientation()[2] * objectPlaceDistance + random.uniform(-objectPlaceNoise, objectPlaceNoise)
        translation[1] = 0.01
        translation[2] -= self.activeRobots['e-puck'].getOrientation()[0] * objectPlaceDistance + random.uniform(-objectPlaceNoise, objectPlaceNoise)
        try:
            ID = random.choice(targetObjects)
            self.loadRobot(kind='button', ID=ID, translation=translation)
            print("supervisor places target object: {}".format(ID))
        except:
            print("no target object")
        self.targetTimer.start()

    if episodeDecision >= targetRate and episodeDecision <= targetRate + distractorRate:
        #place distractor
        translation = transField.getSFVec3f()
        translation[0] -= self.activeRobots['e-puck'].getOrientation()[2] * objectPlaceDistance + random.uniform(-objectPlaceNoise, objectPlaceNoise)
        translation[1] = 0.01
        translation[2] -= self.activeRobots['e-puck'].getOrientation()[0] * objectPlaceDistance + random.uniform(-objectPlaceNoise, objectPlaceNoise)
        try:
            ID = random.choice(distractorObjects)
            self.loadRobot(kind='button', ID=ID, translation=translation)
            print("supervisor places distractor object: {}".format(ID))
        except:
            print("no distractor object")
        self.distractorTimer.start()

    if episodeDecision >= targetRate + distractorRate and distractorRate <= targetRate + distractorRate + queRate:
        #play que sound
        idx = random.choice([i for i,val in enumerate(distractorSounds) if val==1])
        if not self.speaker.isSoundPlaying(""):
            self.sound = frequencies[idx]
            self.speaker.playSound(self.speaker, self.speaker, soundPath+str(frequencies[idx])+"Hz.wav", 1, 1, 0, False)
                    
        print('supervisor plays distractor sound {}Hz'.format(self.sound))
        self.soundTimer.start()
    return 1
    
def phaseEndEpisode(self):
    self.episodeTimer.start()
    return 0
    
phaseComplete = [phasePauseComplete, phaseExploreComplete, phaseTestComplete, phaseTestComplete, phaseTestComplete, phaseSwitchComplete, phaseRepititionComplete, phaseEndComplete]
phaseEpisode = [phasePauseEpisode, phaseExploreEpisode, phaseTestEpisode, phaseTestEpisode, phaseTestEpisode, phaseSwitchEpisode, phaseRepititionEpisode, phaseEndEpisode]

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

def startActionEpisode(self):
    '''starts new action episode depending on phase
    '''
    # reset action Timers
    self.episodeTimer.stop()
    self.episodeTimer.reset()
    self.distractorTimer.stop()
    self.distractorTimer.reset()
    self.targetTimer.stop()
    self.targetTimer.reset()
    self.soundTimer.stop()
    self.soundTimer.reset()
    
    if phaseEpisode[self.phaseList[self.phaseIdx]](self):
        self.phaseEpisode += 1
    self.updateState()

def updatePhase(self):
    # log actions
    if all(a < stateThreshold for a in self.currentState.epuck['action'][:,0]) and any([a > stateThreshold for a in self.currentState.epuck['action'][:,1]]):
        self.currentState.phase['actionEpisode'] += 1
        idx = [i for i,val in enumerate(self.currentState.epuck['action'][:,1]) if val==1][0]
        print("actionEpisode: {}".format(self.currentState.phase['actionEpisode']))
        print("action {} on {}".format(idx, self.currentState.epuck['actionTarget']))
        self.currentState.phase['actionCounter'][self.currentState.epuck['actionTarget'][1]][idx] += 1
        print(self.currentState.phase['actionCounter'])
        self.episodeTimer.start()

    # phase completion conditions
    if phaseComplete[self.phaseList[self.phaseIdx]](self.currentState, self.phaseEpisode, self.clock, self.episodeTimer):
        # new phase
        deleteObjects(self)
        if self.phaseIdx < len(self.phaseList)-1:
            self.phaseIdx += 1
            self.currentState.phase['phase'] = self.phaseList[self.phaseIdx]# init phase
            print("init phase {}".format(self.phaseList[self.phaseIdx]))
            self.phaseEpisode = 0
            self.episodeTimer.reset()
            self.episodeTimer.start()
            self.distractorTimer.stop()
            self.distractorTimer.reset()
            self.targetTimer.stop()
            self.targetTimer.reset()
            self.waitTimer.stop()
            self.waitTimer.reset()
        else:
            # end experiemnt
            print("cleaning up...")
            IDs = []
            for ID in self.activeRobots:
                IDs += [ID]
            for ID in IDs:
                self.deleteRobot(ID)
            print("experiment done...")
            exit()

    # start new action episode
    if self.episodeTimer.reading > episodeTimeout or self.distractorTimer.reading > distractorTimeout or self.soundTimer.reading > soundTimeout or self.targetTimer.reading > targetTimeout:
        deleteObjects(self)
        if not self.waitTimer.run: self.waitTimer.start()
        #print("T{}".format(self.waitTimer.reading-5))
        if self.waitTimer.reading > placeWaitTime:
            self.startActionEpisode()
            self.waitTimer.stop()
            self.waitTimer.reset()

def updateState(self):
    # send task information to epuck and que sounds
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
    self.waitTimer.update()
    # reset epuck if out of bounds
    if abs(self.activeRobots['e-puck'].getPosition()[0]) > resetBound or abs(self.activeRobots['e-puck'].getPosition()[2]) > resetBound:
        transField = self.activeRobots['e-puck'].getField("translation")
        #orienField = self.activeRobots['e-puck'].getField("orientation")
        transField.setSFVec3f([0, 0.0, 0])
