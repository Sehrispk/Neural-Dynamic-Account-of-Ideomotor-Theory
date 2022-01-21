"""SupervisorController controller."""
import time, yaml, random, copy
import numpy as np
from controller import Supervisor
from SupervisorRobot import SupervisorRobot

# load config
f = open('../../worlds/world-setup.yml')
config = yaml.load(f, yaml.FullLoader)
f.close()

# load supervisor
scenario = "voluntaryGoalSwitching"
supervisor = SupervisorRobot(config, scenario)
timestep = int(supervisor.getBasicTimeStep())

# load E-Puck
supervisor.loadRobot(kind='epuck', ID='e-puck')
epuck = supervisor.activeRobots['e-puck']

epuckLEDs = epuck.getFromDevice('led0')
# led 1 ....

# Main loop:
while supervisor.step(timestep) != -1:
    epuck.getPosition()
    epuck.getOrientation()
    epuckLEDS.getState()
    active_objects.getPosition()
    active_objects.getSpeakerState()

    supervisor.update(position, orientation, led, positions, speaker)

    write(self.phase, position, orientation, led, positions, speaker)














    '''if phase == 2 and len(active_objects) == 0:
        translation = epuck.getPosition()
        translation[0] -= epuck.getOrientation()[2] * 0.3
        translation[2] -= epuck.getOrientation()[0] * 0.3
        
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
        exit()'''
        #print(epuck.getPosition()) #[-0.1 bis 0.1] fuer x und y
        #print(np.arccos(epuck.getOrientation()[0])/np.pi*np.sign(epuck.getOrientation()[6]))


# Enter here exit cleanup code.
