def loadRobot(self, kind, ID, translation=[0, 0.01, 0]):
    # creates robotString from config setting, creates robot and returns robot node
    robot_conf = copy.deepcopy(self.config['Robots'][kind])
    try:
        robot_conf['controllerArgs'] = self.config['Scenarios'][self.scenario][ID]
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
    for i in len(self.activeObjects):
        if objectId == self.activeObjects[i].key():
            obj = self.activeObjects.pop(i).value()
            obj.remove()

def chooseActionEpisode(self):
    print('chooseActionEpisode')

def update(self):
    if self.phase == 0:
        if self.init_phase == 1:
            for robotID in self.robotIDs:
                translation = [round(random.uniform(-1, 1), 4), 0.01, round(random.uniform(-1, 1), 4)]
                self.loadRobot(kind='button', ID=robotID, translation=translation)
            emitter.send(bytes(self.phase, 'utf-8'))
            self.init_phase = 0
        else:
            print('wait to finish')
            if finished:
                for i in len(self.active_objects):
                    self.active_objects.pop(0).remove()
                self.phase = 1
                self.init_phase = 1

    elif self.phase == 1:
        # give goal choice command
        if not goal:
            emitter.send(bytes(self.phase, 'utf-8'))
        elif goal:
            self.phase = 2

    elif self.phase == 2:
        translation = epuck.getPosition()
        translation[0] -= epuck.getOrientation()[2] * 0.3
        translation[2] -= epuck.getOrientation()[0] * 0.3
        emitter.send(bytes(2, 'utf-8'))