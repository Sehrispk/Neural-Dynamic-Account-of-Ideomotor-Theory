import copy, random

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

def chooseActionEpisode(self):
    print('chooseActionEpisode')

def update(self):
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
        self.emitter.send(bytes(str(self.phase), 'utf-8'))
        if self.state[2] != -3:
            print('goal selection phase done') 
            self.phase = 2

    elif self.phase == 2:
        #translation = epuck.getPosition()
        #translation[0] -= epuck.getOrientation()[2] * 0.3
        #translation[2] -= epuck.getOrientation()[0] * 0.3
        self.emitter.send(bytes(str(self.phase), 'utf-8'))
        
        
        
        
        
        
        
        
        
        
        
        
        
def inspectState(self):
    while self.receiver.getQueueLength() > 0:
        message = int(str(list(self.receiver.getData())[0]))
        self.receiver.nextPacket()
        if (message >= 500 and message <= 1500) or message == -1:
            self.state[0] = message
        elif (message >=0 and message <= 2) or message == -2:
            self.state[1] = message
        elif (message >= 5 and message <= 15) or message == -3:
            self.state[2] = message
    
    if self.state[1] == -2:
        self.targetObject = ''
    else:
        epuckPosition = self.activeRobots['e-puck'].getPosition()
        obj = ''
        objDistance = 10
        for ID in self.robotIDs:
            objectPosition = self.activeRobots['ID'].getPosition()
            distance = [(epuckPosition[0]-objectPosition[0])**2+(epuckPosition[1]-objectPosition[1])**2]
            if distance < objDistance:
                obj = ID
                objDistance = distance
        self.targetObject = obj
        self.action_counter[obj, action] += 1
        
                
    
            
            
        