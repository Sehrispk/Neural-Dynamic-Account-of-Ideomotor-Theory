"""SupervisorController controller."""

import time, yaml, random, copy
import numpy as np
from controller import Robot
from controller import Supervisor
from utilities import loadRobot

# load supervisor and get nodes
supervisor = Supervisor()
children = supervisor.getRoot().getField('children')
timestep = int(supervisor.getBasicTimeStep())

# load config
f = open('../../worlds/world-setup.yml')
config = yaml.load(f, yaml.FullLoader)
f.close()

# load E-Puck
epuck = loadRobot(children, config['Robots']['epuck'])

# setup experiment
Scenario = "voluntaryGoalSwitching"
phase = -1
if config['Scenarios'][Scenario]['learningPhase'] == True:
    phase = 0
elif config[Scenario]['goalChoicePhase'] == True:
    phase = 1
else:
    phase = 2


# generate object_configs
scenario_objects = config['Scenarios'][Scenario]['objects']
object_configs = []    
active_objects = []
for object in scenario_objects:
    # load color and contingencies
    object_config = copy.deepcopy(config['Robots']['button'])
    object_config['name'] = "\"{}\"".format(object)
    object_config['controllerArgs'] = scenario_objects[object]
    object_configs += [object_config]

# load objects at random location for learnings phase == 0:
if phase == 0:
    for obj_conf in object_configs:
        translation = [round(random.uniform(-1, 1),4), 0.01, round(random.uniform(-1, 1),4)]
        active_objects += [loadRobot(children, obj_conf, translation)]

# Main loop:
tic = time.time()
while supervisor.step(timestep) != -1:
    toc = time.time()
    if phase == 2 and len(active_objects) == 0:
        translation = epuck.getPosition()
        translation[0] = translation[0] - epuck.getOrientation()[2] * 0.3
        translation[2] = translation[2] - epuck.getOrientation()[0] * 0.3
        
        active_objects += [loadRobot(children, object_configs[0], translation)]
    
    
    
    
    # switch phases
    if toc - tic > 10 and phase == 0:
        tic = toc
        for object in active_objects:
            object.remove()
        active_objects.clear()
        print("learning phase done!")
        phase = 1
    
    if toc - tic > 10 and phase == 1:
        tic = toc
        print("goal choice phase done!")
        phase = 2
        
    if toc - tic > 10 and phase == 2:
        tic = toc
        for object in active_objects:
            object.remove()
        active_objects.clear()
        epuck.remove()
        print("scenario done!")
        exit()
        #print(epuck.getPosition()) #[-0.1 bis 0.1] fuer x und y
        #print(np.arccos(epuck.getOrientation()[0])/np.pi*np.sign(epuck.getOrientation()[6]))


# Enter here exit cleanup code.
