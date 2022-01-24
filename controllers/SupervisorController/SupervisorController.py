"""SupervisorController controller."""
import time, yaml
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
'''epuck = supervisor.activeRobots['e-puck']

# get reference to relevant epuck LEDs
epuckLEDs = [epuck.getProtoField('children'), epuck.getProtoField('children'), epuck.getProtoField('children')]
print(epuck.getProtoNumberOfFields())
i=0
field = epuck.getProtoField('children')
while True:
    print(field.getMFNode(i).getDef())
    if field.getMFNode(i).getDef() == 'EPUCK_LED0':
        print(field.getMFNode(i).getBaseTypeName())
        print(field.getMFNode(i).getId())
        print(field.getMFNode(i).getNumberOfFields())
        j=0
        while j < field.getMFNode(i).getNumberOfFields():
            ledField = field.getMFNode(i).getFieldByIndex(j)
            print(ledField.getName())
            j+=1
    i+=1'''
    
# Main loop:
tic = time.time()
while supervisor.step(timestep) != -1:
    # inspect()
    # manage scneario()
    supervisor.inspectState()
    supervisor.managePhases()

    toc = time.time()
    if toc - tic > 100 and supervisor.phase == 0:
        tic = toc
        supervisor.action_counter[:] = 1
        
    if toc - tic > 10 and supervisor.phase == 1:
        tic = toc
        supervisor.state[2] = 15
    # write()














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
