"""SupervisorController controller."""

# Webots todo!!!!
# (TUNING OF TIMERS)

#DFT Tuning/todos
# MEMORY FOR COLORS: TODAY
# TUNING OF BELIEF STRUCTURE
# desire in DFT architecture?
# Attention



# goal selection phase after each action episode?



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

f_traj.write("{}\t{}\t{}\t{}\t{}\n".format("Time", "e-puck", supervisor.robotIDs[0], supervisor.robotIDs[1], supervisor.robotIDs[2]))
f_ev.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format("Time", "phase", "actionEpisode", "goal", "action", "target", "sound"))

# Main loop:
tic = time.time()
init = 0
while supervisor.step(timestep) != -1:
    supervisor.updateState()
    supervisor.updatePhase()

    toc = time.time()
    if toc - tic > 3 and supervisor.currentState.phase['phase'] == 0 and not init:
        tic = toc
        init=1
        supervisor.initPhase()
    
    #if toc - tic > 30 and supervisor.currentState.phase['phase'] == 0:
    #    tic = toc
    #    supervisor.currentState.phase['phase'] = 1
    #    supervisor.initPhase()
        
    #if toc - tic > 60 and supervisor.currentState.phase['phase'] == 1:
    #    tic = toc
    #    supervisor.currentState.phase['phase'] = 2
    #    supervisor.initPhase()

    # write data
    positions = "{} {} {}".format(supervisor.currentState.epuck['position'], supervisor.currentState.epuck['orientation'], supervisor.currentState.epuck['led'])
    for ID in supervisor.robotIDs:
        if isActive(ID, supervisor):
            positions += "\t{}".format(supervisor.currentState.objects[ID]['position'])
        else:
            positions += "\t"

    f_traj.write("{}\t{}\n".format(supervisor.clock.reading, positions))
    f_traj.flush()

    sound = np.zeros(10)
    for ID in supervisor.robotIDs:
        if isActive(ID, supervisor):
            if any(supervisor.currentState.objects[ID]['sound']) != 0:
                sound = supervisor.currentState.objects[ID]['sound']

    f_ev.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(supervisor.clock.reading, supervisor.currentState.phase['phase'],
                                           supervisor.currentState.phase['actionEpisode'],
                                           supervisor.currentState.epuck['goal'],
                                           supervisor.currentState.epuck['action'][:,0],
                                           supervisor.currentState.epuck['actionTarget'][0],
                                           sound))
    f_ev.flush()

f_traj.close()
f_ev.close()
