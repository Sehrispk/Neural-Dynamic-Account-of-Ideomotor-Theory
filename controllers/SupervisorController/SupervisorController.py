"""SupervisorController controller."""
import time, yaml
import numpy as np
from controller import Supervisor
from SupervisorRobot import SupervisorRobot

def isActive(ID, supervisor):
    try:
        supervisor.activeRobots[ID]
        return 1
    except:
        return 0

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
supervisor.currentState.epuck['action'] = np.zeros((3,2))
supervisor.currentState.epuck['actionTarget'] = ['','']
supervisor.currentState.epuck['position'] = np.zeros(3)

# prepare Data
f_traj = open("../../data/trajectory.dat", 'w')
f_ev = open("../../data/events.dat", 'w')

f_traj.write("{}\t{}\t{}\t{}\n".format("e-puck", supervisor.robotIDs[0], supervisor.robotIDs[1], supervisor.robotIDs[2]))
f_ev.write("{}\t{}\t{}\t{}\t{}\n".format("phase", "actionEpisode", "goal", "action", "target", "sound"))

# Main loop:
tic = time.time()
init = 0
while supervisor.step(timestep) != -1:
    supervisor.updateState()
    supervisor.updatePhase()

    toc = time.time()
    if toc - tic > 10 and supervisor.currentState.phase['phase'] == 0 and not init:
        tic = toc
        init=1
        supervisor.initPhase()
        supervisor.updateState()
    
    if toc - tic > 300 and supervisor.currentState.phase['phase'] == 0:
        tic = toc
        supervisor.currentState.phase['phase'] = 1
        supervisor.initPhase()
        supervisor.updateState()
        
    if toc - tic > 300 and supervisor.currentState.phase['phase'] == 1:
        tic = toc
        supervisor.currentState.phase['phase'] = 2
        supervisor.initPhase()
        supervisor.updateState()

    # write data
    positions = "{} {}".format(supervisor.currentState.epuck['position'], supervisor.currentState.epuck['orientation'])
    for ID in supervisor.robotIDs:
        if isActive(ID, supervisor):
            positions += "\t{}".format(supervisor.currentState.objects[ID]['position'])
        else:
            positions += "\t"

    f_traj.write("{}\n".format(positions))
    f_traj.flush()

    sound = 0
    for ID in supervisor.robotIDs:
        if isActive(ID, supervisor):
            if supervisor.currentState.objects[ID]['sound'] != 0:
                sound = supervisor.currentState.objects['ID']['position']

    f_ev.write("{}\t{}\t{}\t{}\t{}\n".format(supervisor.currentState.phase['phase'],
                                           supervisor.currentState.phase['actionEpisode'],
                                           supervisor.currentState.epuck['goal'],
                                           supervisor.currentState.epuck['action'][:,0],
                                           supervisor.currentState.epuck['actionTarget'][0],
                                           sound))
    f_ev.flush()

f_traj.close()
f_ev.close()
